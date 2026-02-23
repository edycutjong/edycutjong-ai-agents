"""Tests for IP Lookup."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.lookup import lookup, is_ipv4, is_ipv6, cidr_info, is_in_range, format_result_markdown

def test_valid(): r = lookup("8.8.8.8"); assert r.is_valid and r.version == 4
def test_private(): r = lookup("192.168.1.1"); assert r.is_private
def test_public(): r = lookup("8.8.8.8"); assert not r.is_private
def test_loopback(): r = lookup("127.0.0.1"); assert r.is_loopback
def test_ipv6(): r = lookup("::1"); assert r.version == 6 and r.is_loopback
def test_invalid(): r = lookup("not-an-ip"); assert not r.is_valid
def test_is_ipv4(): assert is_ipv4("1.2.3.4")
def test_not_ipv4(): assert not is_ipv4("::1")
def test_is_ipv6(): assert is_ipv6("::1")
def test_not_ipv6(): assert not is_ipv6("1.2.3.4")
def test_cidr(): d = cidr_info("192.168.1.0/24"); assert d["num_hosts"] == 254
def test_cidr_prefix(): d = cidr_info("10.0.0.0/8"); assert d["prefix_len"] == 8
def test_in_range(): assert is_in_range("192.168.1.50", "192.168.1.0/24")
def test_not_in_range(): assert not is_in_range("10.0.0.1", "192.168.1.0/24")
def test_binary(): r = lookup("1.0.0.1"); assert len(r.binary) == 32
def test_format(): md = format_result_markdown(lookup("8.8.8.8")); assert "IP Lookup" in md
def test_to_dict(): d = lookup("8.8.8.8").to_dict(); assert "version" in d
