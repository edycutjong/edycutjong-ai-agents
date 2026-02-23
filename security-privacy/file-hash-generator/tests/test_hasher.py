"""Tests for File Hash Generator."""
import sys, os, hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.hasher import hash_text, hash_bytes, verify_hash, compare_hashes, checksum, format_result_markdown, ALGORITHMS

def test_sha256(): r = hash_text("hello"); assert len(r.hashes["sha256"]) == 64
def test_md5(): r = hash_text("hello"); assert len(r.hashes["md5"]) == 32
def test_sha1(): r = hash_text("hello"); assert len(r.hashes["sha1"]) == 40
def test_all_algos(): r = hash_text("test"); assert len(r.hashes) == len(ALGORITHMS)
def test_primary(): r = hash_text("test", "md5"); assert r.primary == r.hashes["md5"]
def test_size(): r = hash_text("hello"); assert r.data_size == 5
def test_deterministic(): a = hash_text("x"); b = hash_text("x"); assert a.hashes["sha256"] == b.hashes["sha256"]
def test_different(): a = hash_text("x"); b = hash_text("y"); assert a.hashes["sha256"] != b.hashes["sha256"]
def test_bytes(): h = hash_bytes(b"hello", "sha256"); assert len(h) == 64
def test_verify_ok(): h = hashlib.sha256(b"test").hexdigest(); assert verify_hash("test", h)
def test_verify_fail(): assert not verify_hash("test", "wronghash")
def test_compare_same(): assert compare_hashes("hello", "hello")
def test_compare_diff(): assert not compare_hashes("hello", "world")
def test_checksum(): c = checksum("test"); assert len(c) == 8
def test_format(): md = format_result_markdown(hash_text("test")); assert "Hash Generator" in md
def test_to_dict(): d = hash_text("test").to_dict(); assert "sha256" in d
