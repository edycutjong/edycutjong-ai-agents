"""IP geolocation lookup — parse and validate IP addresses with mock geolocation data."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

@dataclass
class IPInfo:
    ip: str = ""; version: int = 0; is_valid: bool = False; is_private: bool = False
    country: str = ""; city: str = ""; isp: str = ""; error: str = ""
    def to_dict(self) -> dict: return {"ip": self.ip, "version": self.version, "is_valid": self.is_valid, "is_private": self.is_private, "country": self.country}

PRIVATE_RANGES_V4 = [("10.0.0.0", "10.255.255.255"), ("172.16.0.0", "172.31.255.255"), ("192.168.0.0", "192.168.255.255"), ("127.0.0.0", "127.255.255.255")]
MOCK_GEO = {"8.8.8.8": ("US", "Mountain View", "Google"), "1.1.1.1": ("AU", "Sydney", "Cloudflare"), "208.67.222.222": ("US", "San Francisco", "OpenDNS"), "9.9.9.9": ("US", "Berkeley", "Quad9")}

def ip_to_int(ip: str) -> int:
    parts = ip.split(".")
    return sum(int(p) << (8 * (3 - i)) for i, p in enumerate(parts))

def validate_ipv4(ip: str) -> bool:
    m = re.match(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$', ip)
    if not m: return False
    return all(0 <= int(g) <= 255 for g in m.groups())

def validate_ipv6(ip: str) -> bool:
    try:
        parts = ip.split(":")
        if len(parts) > 8: return False
        if "::" in ip: return True  # simplified check
        return len(parts) == 8 and all(len(p) <= 4 for p in parts)
    except: return False

def is_private(ip: str) -> bool:
    if not validate_ipv4(ip): return False
    n = ip_to_int(ip)
    for start, end in PRIVATE_RANGES_V4:
        if ip_to_int(start) <= n <= ip_to_int(end): return True
    return False

def lookup_ip(ip: str) -> IPInfo:
    r = IPInfo(ip=ip)
    if validate_ipv4(ip):
        r.version = 4; r.is_valid = True; r.is_private = is_private(ip)
        if ip in MOCK_GEO:
            r.country, r.city, r.isp = MOCK_GEO[ip]
        elif r.is_private:
            r.country = "Private"; r.city = "Local"
    elif validate_ipv6(ip):
        r.version = 6; r.is_valid = True
        r.country = "IPv6"
    else:
        r.error = "Invalid IP address"
    return r

@dataclass
class BatchResult:
    results: list[IPInfo] = field(default_factory=list)
    total: int = 0; valid: int = 0; private: int = 0

def batch_lookup(ips: list[str]) -> BatchResult:
    b = BatchResult(total=len(ips))
    for ip in ips:
        r = lookup_ip(ip)
        b.results.append(r)
        if r.is_valid: b.valid += 1
        if r.is_private: b.private += 1
    return b

def format_result_markdown(r: IPInfo) -> str:
    if not r.is_valid: return f"## IP Lookup ❌\n**IP:** `{r.ip}` | **Error:** {r.error}"
    emoji = "🏠" if r.is_private else "🌍"
    lines = [f"## IP Lookup {emoji}", f"**IP:** `{r.ip}` | **Version:** IPv{r.version} | **Private:** {r.is_private}", ""]
    if r.country: lines.append(f"**Location:** {r.city}, {r.country}")
    if r.isp: lines.append(f"**ISP:** {r.isp}")
    return "\n".join(lines)
