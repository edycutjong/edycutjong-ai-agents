"""Port scanner simulator — analyze port configurations and common service detection."""
from __future__ import annotations
from dataclasses import dataclass, field

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 9200: "Elasticsearch", 27017: "MongoDB",
}
RISKY_PORTS = {21, 23, 25, 445, 3389, 5900}

@dataclass
class PortInfo:
    port: int; service: str = ""; is_common: bool = False; is_risky: bool = False; protocol: str = "tcp"

@dataclass
class ScanResult:
    target: str = ""; ports: list[PortInfo] = field(default_factory=list)
    open_count: int = 0; risky_count: int = 0; issues: list[str] = field(default_factory=list)
    def to_dict(self) -> dict: return {"target": self.target, "open_count": self.open_count, "risky_count": self.risky_count}

def identify_port(port: int) -> PortInfo:
    service = COMMON_PORTS.get(port, "Unknown")
    return PortInfo(port=port, service=service, is_common=port in COMMON_PORTS, is_risky=port in RISKY_PORTS)

def analyze_ports(ports: list[int], target: str = "localhost") -> ScanResult:
    r = ScanResult(target=target, open_count=len(ports))
    for p in sorted(set(ports)):
        info = identify_port(p)
        r.ports.append(info)
        if info.is_risky:
            r.risky_count += 1
            r.issues.append(f"Port {p} ({info.service}) is a security risk")
    if 23 in ports: r.issues.append("Telnet (23) transmits data in plaintext — use SSH instead")
    if 21 in ports: r.issues.append("FTP (21) is insecure — use SFTP instead")
    if 80 in ports and 443 not in ports: r.issues.append("HTTP without HTTPS — add TLS")
    return r

def suggest_firewall_rules(ports: list[int]) -> list[str]:
    rules = []
    for p in sorted(set(ports)):
        info = identify_port(p)
        if info.is_risky: rules.append(f"DENY {p}/tcp  # {info.service} — security risk")
        elif info.is_common: rules.append(f"ALLOW {p}/tcp  # {info.service}")
        else: rules.append(f"REVIEW {p}/tcp  # Unknown service")
    return rules

def get_port_range(start: int, end: int) -> list[PortInfo]:
    return [identify_port(p) for p in range(start, end + 1) if p in COMMON_PORTS]

def format_result_markdown(r: ScanResult) -> str:
    emoji = "🟢" if r.risky_count == 0 else "🔴"
    lines = [f"## Port Scan {emoji}", f"**Target:** {r.target} | **Open:** {r.open_count} | **Risky:** {r.risky_count}", ""]
    for p in r.ports:
        risk = " ⚠️" if p.is_risky else ""
        lines.append(f"- Port {p.port}: {p.service}{risk}")
    if r.issues:
        lines.append("\n### Security Issues")
        for i in r.issues: lines.append(f"- 🔴 {i}")
    return "\n".join(lines)
