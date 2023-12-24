# -*- coding: utf-8 -*-
import typing as ty
import urllib.parse

import lektor.pluginsystem
import lektor.publisher

import httpx
import ipfshttpclient
import ipfshttpclient.encoding
import lexicon.client
import lexicon.config


def decode_multi_json_response(resp: httpx.Response) -> ty.Generator[dict, ty.Any, None]:
	decoder = ipfshttpclient.encoding.get_encoding("json")
	for chunk in resp.iter_bytes():
		yield from decoder.parse_partial(chunk)
	yield from decoder.parse_finalize()


class IpfsUploader:
	def __init__(self, opts):
		self.addr = opts.get("ipfs-api-addr", ipfshttpclient.DEFAULT_ADDR)
		self.base = opts.get("ipfs-api-base", ipfshttpclient.DEFAULT_BASE)
		self.username = opts.get("ipfs-api-username")
		self.password = opts.get("ipfs-api-password")
	
	def upload(self, target_dir, *, ipns_key: ty.Optional[str] = None) -> ty.Generator[str, ty.Any, ty.Tuple[str, ty.Optional[str]]]:
		with ipfshttpclient.connect(self.addr, self.base, username=self.username, password=self.password) as client:
			yield "Adding all files to IPFS daemon"
			cid = client.add(target_dir, recursive=True, period_special=False, cid_version=1, raw_leaves=True)[-1]["Hash"]
			
			if ipns_key is not None:
				yield f"Publishing /ipfs/{cid} at IPNS key “{ipns_key}”"
				ipns_key = client.name.publish(f"/ipfs/{cid}", key=ipns_key)["Name"]
			
			return cid, ipns_key

class IpfsClusterUploader(IpfsUploader):
	def __init__(self, opts):
		super().__init__(opts)
		
		self.cluster_endpoint = opts.get("cluster-endpoint", "http://localhost:9094/")
		#XXX: Which exception type to raise on invalid config?
		self.cluster_pin_name = opts["cluster-pin-name"]
	
	def upload(self, target_dir, **kwargs) -> ty.Generator[str, ty.Any, ty.Tuple[str, ty.Optional[str]]]:
		with httpx.Client(base_url=self.cluster_endpoint) as client:
			# Find current CID pinned by cluster pin name
			yield f"Asking IPFS Cluster daemon for current allocation of name “{self.cluster_pin_name}”"
			old_cid: ty.Optional[str] = None
			for allocation in decode_multi_json_response(client.get("allocations")):
				if allocation.get("type") == "pin" and allocation["name"] == self.cluster_pin_name:
					old_cid = allocation["cid"]
					break
			
			# Talk with associated IPFS daemon directly to upload files, yielding
			# the CID of the added files
			new_cid, ipns_key = yield from super().upload(target_dir, **kwargs)
			
			# Ask the cluster instance to add or update the associated pin
			if old_cid is None:
				yield f"Pinning {new_cid} as “{self.cluster_pin_name}” in cluster"
				quoted_name = urllib.parse.quote(self.cluster_pin_name)
				client.post(f"pins/ipfs/{new_cid}?mode=recursive&name={quoted_name}").json()
			elif old_cid != new_cid:
				yield f"Pinning {new_cid} as “{self.cluster_pin_name}” in cluster (replacing {old_cid})"
				client.post(f"pins/ipfs/{new_cid}?mode=recursive&pin-update={old_cid}").json()
				client.delete(f"pins/ipfs/{old_cid}").json()
			else:
				yield f"Content is unchanged, not updating cluster pin"
			
			return new_cid, ipns_key


def uploader_for_upload_type(upload_type, *args, **kwargs):
	if upload_type == "ipfs":
		return IpfsUploader(*args, **kwargs)
	elif upload_type == "ipfs-cluster":
		return IpfsClusterUploader(*args, **kwargs)
	else:
		#XXX: Which exception type to raise on invalid config?
		raise Exception(f"Unsupported server upload-type: {upload_type}")


class IpfsDnsLinkPublisherConfigSource(lexicon.config.ConfigSource):
	"""Lexicon config source mapping queries to keys of the given Lektor server
	   configuration section"""
	def __init__(self, server_info: "lektor.environment.config.ServerInfo") -> None:
		super().__init__()
		self._opts = server_info.extra
	
	def resolve(self, config_key: str) -> ty.Optional[ty.Any]:
		# Ignores provider name when resolving keys since our Lexicon
		# configuration is intended to only target exactly one DNS provider
		name = "dns-" + (config_key.rsplit(":", 1)[-1].replace("_", "-"))
		return self._opts.get(name, None)


def make_lexicon_config(
		host: str,
		server_info: "lektor.environment.config.ServerInfo",
		extra_dict: ty.Dict[str, ty.Any],
) -> lexicon.config.ConfigResolver:
	return lexicon.config.ConfigResolver().with_env() \
	       .with_config_source(IpfsDnsLinkPublisherConfigSource(server_info)) \
	       .with_dict({
	           "domain": f"_dnslink.{host}",
	           "name": f"_dnslink.{host}",
	           "type": "TXT",
	           **extra_dict
	       })


class IpfsPublisher(lektor.publisher.Publisher):
	def publish(self, target_uri, credentials, server_info: "lektor.environment.config.ServerInfo", **extra) \
	    -> ty.Generator[str, ty.Any, str]:
		yield "Note: This publisher will not reference your published site anywhere! For supported publishing flows it will be more convenient to use “ipfs+dnslink://…” or “ipns://…” instead!"
		assert target_uri.host is None, "ipfs:// publisher does not expect any target name"
		
		# Add static files to IPFS (and optionally IPFS-Cluster)
		uploader = uploader_for_upload_type(server_info.extra.get("upload-type", "ipfs"), server_info.extra)
		cid, _ = yield from uploader.upload(self.output_path)
		
		yield f"Publishing to “/ipfs/{cid}” completed successfully! Please update your references!"


class IpfsDnsLinkPublisher(lektor.publisher.Publisher):
	def publish(self, target_uri, credentials, server_info: "lektor.environment.config.ServerInfo", **extra) \
	    -> ty.Generator[str, ty.Any, str]:
		target_host = target_uri.host
		
		# Add static files to IPFS (and optionally IPFS-Cluster)
		uploader = uploader_for_upload_type(server_info.extra.get("upload-type", "ipfs"), server_info.extra)
		cid, _ = yield from uploader.upload(self.output_path)
		
		# Assemble lexicon request options that are the same for all
		yield f"Looking for existing DNSLink record on “{target_host}”"
		content = f"dnslink=/ipfs/{cid}"
		result = lexicon.client.Client(
			make_lexicon_config(target_host, server_info, {"action": "list"}),
		).execute()
		if len(result) > 0:
			yield f"Replacing DNSLink record on “{target_host}” with “{content}”"
			lexicon.client.Client(
				make_lexicon_config(target_host, server_info, {
					"action": "update", "identifer": result[0]["id"], "content": content,
				}),
			).execute()
		else:
			yield f"Creating DNSLink record on “{target_host}” with “{content}”"
			lexicon.client.Client(
				make_lexicon_config(target_host, server_info, {
					"action": "create", "content": content,
				}),
			).execute()
		yield f"Publishing to “{target_uri}” completed successfully!"


class IpnsPublisher(lektor.publisher.Publisher):
	def publish(self, target_uri, credentials, server_info: "lektor.environment.config.ServerInfo", **extra) \
	    -> ty.Generator[str, ty.Any, str]:
		ipns_key = target_uri.host
	    
		# Add static files to IPFS (and optionally IPFS-Cluster)
		#
		# This also adds the IPNS reference in the same call to reuse the IPFS
		# client connection and related code between both steps.
		uploader = uploader_for_upload_type(server_info.extra.get("upload-type", "ipfs"), server_info.extra)
		cid, ipns_key = yield from uploader.upload(self.output_path, ipns_key=ipns_key)
		
		yield f"Publishing to “/ipns/{ipns_key}” completed successfully!"


class IpfsDeployPlugin(lektor.pluginsystem.Plugin):
	name = "deploy-ipfs"
	description = "Deploy your static Lektor website to IPFS!"
	
	def on_setup_env(self, **extra):
		for scheme, impl in (
				("ipfs", IpfsPublisher),
				("ipfs+dnslink", IpfsDnsLinkPublisher),
				("ipns", IpnsPublisher),
		):
			# Lektor 2.0+
			self.env.add_publisher(scheme, impl)
