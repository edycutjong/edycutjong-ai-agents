"""Tests for Port Scanner."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.scanner import identify_port, analyze_ports, suggest_firewall_rules, get_port_range, format_result_markdown, COMMON_PORTS, RISKY_PORTS

def test_ssh(): p = identify_port(22); assert p.service == "SSH" and p.is_common
def test_http(): p = identify_port(80); assert p.service == "HTTP"
def test_https(): p = identify_port(443); assert p.service == "HTTPS"
def test_unknown(): p = identify_port(12345); assert p.service == "Unknown" and not p.is_common
def test_risky_telnet(): p = identify_port(23); assert p.is_risky
def test_risky_ftp(): p = identify_port(21); assert p.is_risky
def test_safe_ssh(): p = identify_port(22); assert not p.is_risky
def test_analyze(): r = analyze_ports([80, 443]); assert r.open_count == 2 and r.risky_count == 0
def test_analyze_risky(): r = analyze_ports([23, 80]); assert r.risky_count >= 1
def test_telnet_issue(): r = analyze_ports([23]); assert any("Telnet" in i for i in r.issues)
def test_ftp_issue(): r = analyze_ports([21]); assert any("FTP" in i for i in r.issues)
def test_http_no_https(): r = analyze_ports([80]); assert any("HTTPS" in i for i in r.issues)
def test_firewall(): rules = suggest_firewall_rules([22, 23]); assert any("DENY" in r for r in rules)
def test_firewall_allow(): rules = suggest_firewall_rules([22]); assert any("ALLOW" in r for r in rules)
def test_port_range(): pr = get_port_range(20, 25); assert len(pr) >= 2
def test_common_count(): assert len(COMMON_PORTS) >= 20
def test_format(): md = format_result_markdown(analyze_ports([80, 443])); assert "Port Scan" in md
def test_to_dict(): d = analyze_ports([80]).to_dict(); assert "open_count" in d
