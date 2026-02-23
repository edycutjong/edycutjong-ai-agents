"""Tests for IP Geolocation Lookup."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.lookup import lookup_ip, validate_ipv4, validate_ipv6, is_private, ip_to_int, batch_lookup, format_result_markdown

def test_valid_ipv4(): assert validate_ipv4("8.8.8.8")
def test_invalid_ipv4(): assert not validate_ipv4("999.999.999.999")
def test_invalid_format(): assert not validate_ipv4("not an ip")
def test_valid_ipv6(): assert validate_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
def test_ipv6_short(): assert validate_ipv6("::1")
def test_ip_to_int(): assert ip_to_int("0.0.0.1") == 1
def test_private_10(): assert is_private("10.0.0.1")
def test_private_192(): assert is_private("192.168.1.1")
def test_private_172(): assert is_private("172.16.0.1")
def test_private_127(): assert is_private("127.0.0.1")
def test_public(): assert not is_private("8.8.8.8")
def test_lookup_google(): r = lookup_ip("8.8.8.8"); assert r.country == "US" and r.isp == "Google"
def test_lookup_cloudflare(): r = lookup_ip("1.1.1.1"); assert r.country == "AU"
def test_lookup_private(): r = lookup_ip("192.168.1.1"); assert r.is_private and r.country == "Private"
def test_lookup_invalid(): r = lookup_ip("bad"); assert not r.is_valid
def test_batch(): b = batch_lookup(["8.8.8.8", "192.168.1.1", "bad"]); assert b.valid == 2 and b.private == 1
def test_format(): md = format_result_markdown(lookup_ip("8.8.8.8")); assert "IP Lookup" in md
def test_format_invalid(): md = format_result_markdown(lookup_ip("bad")); assert "❌" in md
def test_to_dict(): d = lookup_ip("8.8.8.8").to_dict(); assert "country" in d
