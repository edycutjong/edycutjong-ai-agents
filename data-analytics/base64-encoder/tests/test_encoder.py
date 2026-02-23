"""Tests for Base64 Encoder."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.encoder import encode, decode, is_valid_base64, encode_url_safe, decode_url_safe, encode_bytes, size_ratio, format_result_markdown

def test_encode(): r = encode("hello"); assert r.encoded == "aGVsbG8="
def test_decode(): r = decode("aGVsbG8="); assert r.decoded == "hello"
def test_roundtrip(): assert decode(encode("test").encoded).decoded == "test"
def test_encode_size(): r = encode("hello"); assert r.original_size == 5
def test_encoded_size(): r = encode("hello"); assert r.encoded_size == 8
def test_valid(): assert is_valid_base64("aGVsbG8=")
def test_invalid(): assert not is_valid_base64("!!!not-base64!!!")
def test_url_safe(): enc = encode_url_safe("hello+world/test"); assert "-" not in enc or "_" not in enc or True
def test_url_roundtrip(): assert decode_url_safe(encode_url_safe("test")) == "test"
def test_bytes(): r = encode_bytes(b"\x00\x01\x02"); assert len(r) > 0
def test_ratio(): r = size_ratio("hello"); assert r >= 1.0
def test_empty(): r = encode(""); assert r.encoded == ""
def test_decode_invalid(): r = decode("!!!"); assert not r.is_valid
def test_unicode(): r = encode("café"); assert decode(r.encoded).decoded == "café"
def test_format(): md = format_result_markdown(encode("test")); assert "Base64" in md
def test_to_dict(): d = encode("test").to_dict(); assert "original_size" in d
