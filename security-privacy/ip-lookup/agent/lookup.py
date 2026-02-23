"""IP lookup — parse, validate, and analyze IP addresses."""
from __future__ import annotations
import ipaddress, re
from dataclasses import dataclass

@dataclass
class IPResult:
    address: str = ""; version: int = 0; is_private: bool = False; is_loopback: bool = False
    is_valid: bool = True; network: str = ""; error: str = ""; binary: str = ""
    def to_dict(self) -> dict: return {"address": self.address, "version": self.version, "is_private": self.is_private, "is_valid": self.is_valid}

def lookup(ip: str) -> IPResult:
    r = IPResult(address=ip.strip())
    try:
        addr = ipaddress.ip_address(r.address)
        r.version = addr.version; r.is_private = addr.is_private; r.is_loopback = addr.is_loopback
        r.binary = bin(int(addr))[2:].zfill(32 if r.version == 4 else 128)
    except ValueError as e:
        r.is_valid = False; r.error = str(e)
    return r

def is_ipv4(ip: str) -> bool:
    try: return ipaddress.ip_address(ip).version == 4
    except: return False

def is_ipv6(ip: str) -> bool:
    try: return ipaddress.ip_address(ip).version == 6
    except: return False

def cidr_info(cidr: str) -> dict:
    try:
        net = ipaddress.ip_network(cidr, strict=False)
        return {"network": str(net.network_address), "broadcast": str(net.broadcast_address), "num_hosts": net.num_addresses - 2 if net.version == 4 else net.num_addresses, "prefix_len": net.prefixlen}
    except: return {}

def is_in_range(ip: str, cidr: str) -> bool:
    try: return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr, strict=False)
    except: return False

def format_result_markdown(r: IPResult) -> str:
    if not r.is_valid: return f"## IP Lookup ❌\n**Error:** {r.error}"
    return f"## IP Lookup 🌐\n**IP:** `{r.address}` | **v{r.version}** | Private: {r.is_private} | Loopback: {r.is_loopback}"
