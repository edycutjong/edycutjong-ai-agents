"""Tests for JWT Decoder."""
import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.decoder import decode_jwt, get_claims, get_header, is_expired, _make_test_token, format_result_markdown

VALID_TOKEN = _make_test_token({"alg": "HS256", "typ": "JWT"}, {"sub": "1234", "name": "Test", "exp": int(time.time()) + 3600})
EXPIRED_TOKEN = _make_test_token({"alg": "HS256", "typ": "JWT"}, {"sub": "1234", "exp": 1000000})

def test_decode(): r = decode_jwt(VALID_TOKEN); assert r.is_valid
def test_header(): r = decode_jwt(VALID_TOKEN); assert r.header["alg"] == "HS256"
def test_payload(): r = decode_jwt(VALID_TOKEN); assert r.payload["sub"] == "1234"
def test_algorithm(): r = decode_jwt(VALID_TOKEN); assert r.algorithm == "HS256"
def test_not_expired(): r = decode_jwt(VALID_TOKEN); assert not r.is_expired
def test_expired(): r = decode_jwt(EXPIRED_TOKEN); assert r.is_expired
def test_invalid(): r = decode_jwt("not.a.jwt"); assert not r.is_valid
def test_bad_structure(): r = decode_jwt("onlyone"); assert not r.is_valid
def test_claims(): c = get_claims(VALID_TOKEN); assert "sub" in c
def test_get_header(): h = get_header(VALID_TOKEN); assert "alg" in h
def test_is_expired_func(): assert is_expired(EXPIRED_TOKEN)
def test_not_expired_func(): assert not is_expired(VALID_TOKEN)
def test_format(): md = format_result_markdown(decode_jwt(VALID_TOKEN)); assert "JWT Decoder" in md
def test_to_dict(): d = decode_jwt(VALID_TOKEN).to_dict(); assert "algorithm" in d
