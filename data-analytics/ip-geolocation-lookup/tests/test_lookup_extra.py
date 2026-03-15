import os
from agent.lookup import validate_ipv6, lookup_ip
import config

def test_config():
    assert config.Config is not None

def test_validate_ipv6_exception():
    # Trigger exception in validate_ipv6
    # ip.split(":") throws AttributeError if ip is not a string
    assert not validate_ipv6(12345)

def test_lookup_ipv6():
    # cover lines 48-49 in lookup_ip
    r = lookup_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    assert r.version == 6
    assert r.is_valid is True
    assert r.country == "IPv6"
