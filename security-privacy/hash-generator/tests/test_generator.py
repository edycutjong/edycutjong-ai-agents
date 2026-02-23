"""Tests for Hash Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import generate_hash, hash_file_bytes, verify_hash, multi_hash, compare_hashes, detect_algorithm, format_result_markdown, ALGORITHMS

def test_sha256(): r = generate_hash("hello"); assert r.algorithm == "sha256" and len(r.hash_value) == 64
def test_md5(): r = generate_hash("hello", "md5"); assert len(r.hash_value) == 32
def test_sha1(): r = generate_hash("hello", "sha1"); assert len(r.hash_value) == 40
def test_sha512(): r = generate_hash("hello", "sha512"); assert len(r.hash_value) == 128
def test_deterministic(): assert generate_hash("test").hash_value == generate_hash("test").hash_value
def test_different(): assert generate_hash("a").hash_value != generate_hash("b").hash_value
def test_file_bytes(): h = hash_file_bytes(b"hello"); assert len(h) == 64
def test_verify_ok(): h = generate_hash("hello").hash_value; assert verify_hash("hello", h)
def test_verify_fail(): assert not verify_hash("hello", "wrong_hash")
def test_multi(): m = multi_hash("hello"); assert len(m) >= 4 and "sha256" in m
def test_compare_ok(): assert compare_hashes("abc123", "ABC123")
def test_compare_fail(): assert not compare_hashes("abc", "def")
def test_detect_md5(): assert detect_algorithm("d" * 32) == "md5"
def test_detect_sha256(): assert detect_algorithm("d" * 64) == "sha256"
def test_detect_unknown(): assert detect_algorithm("short") == "unknown"
def test_format(): md = format_result_markdown(generate_hash("test")); assert "Hash Generator" in md
def test_to_dict(): d = generate_hash("test").to_dict(); assert "hash" in d
def test_algos(): assert len(ALGORITHMS) >= 4
