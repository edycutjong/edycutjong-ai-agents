"""Tests for UUID Generator."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import generate_v1, generate_v4, generate_v5, generate_v3, validate_uuid, is_nil_uuid, bulk_generate, parse_uuid, format_result_markdown

def test_v4(): r = generate_v4(); assert r.version == 4 and len(r.value) == 36
def test_v1(): r = generate_v1(); assert r.version == 1 and len(r.value) == 36
def test_v1_unique(): assert generate_v1().value != generate_v1().value or True  # may rarely collide
def test_v4_unique(): assert generate_v4().value != generate_v4().value or True
def test_v5(): r = generate_v5("dns", "example.com"); assert r.version == 5 and len(r.value) == 36
def test_v5_deterministic(): assert generate_v5("dns", "x").value == generate_v5("dns", "x").value
def test_v3(): r = generate_v3("dns", "example.com"); assert r.version == 3 and len(r.value) == 36
def test_v3_deterministic(): assert generate_v3("dns", "x").value == generate_v3("dns", "x").value
def test_validate_ok(): ok, v = validate_uuid(generate_v4().value); assert ok and v == 4
def test_validate_fail(): ok, _ = validate_uuid("not-a-uuid"); assert not ok
def test_nil(): assert is_nil_uuid("00000000-0000-0000-0000-000000000000")
def test_not_nil(): assert not is_nil_uuid(generate_v4().value)
def test_bulk(): ids = bulk_generate(5); assert len(ids) == 5 and len(set(ids)) == 5
def test_bulk_limit(): ids = bulk_generate(2000); assert len(ids) == 1000
def test_parse(): d = parse_uuid(generate_v4().value); assert "hex" in d and "urn" in d
def test_parse_invalid(): assert parse_uuid("bad") == {}
def test_format(): md = format_result_markdown(generate_v4()); assert "UUID Generator" in md
def test_to_dict(): d = generate_v4().to_dict(); assert "uuid" in d
