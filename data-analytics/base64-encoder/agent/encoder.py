"""Base64 encoder/decoder — encode, decode, and validate Base64 data."""
from __future__ import annotations
import base64
from dataclasses import dataclass

@dataclass
class Base64Result:
    original: str = ""; encoded: str = ""; decoded: str = ""; is_valid: bool = True
    original_size: int = 0; encoded_size: int = 0; error: str = ""
    def to_dict(self) -> dict: return {"original_size": self.original_size, "encoded_size": self.encoded_size, "is_valid": self.is_valid}

def encode(text: str) -> Base64Result:
    data = text.encode()
    enc = base64.b64encode(data).decode()
    return Base64Result(original=text, encoded=enc, original_size=len(data), encoded_size=len(enc))

def decode(b64: str) -> Base64Result:
    r = Base64Result(encoded=b64, encoded_size=len(b64))
    try:
        data = base64.b64decode(b64, validate=True)
        r.decoded = data.decode(); r.original_size = len(data)
    except Exception as e:
        r.is_valid = False; r.error = str(e)
    return r

def is_valid_base64(text: str) -> bool:
    try: base64.b64decode(text, validate=True); return True
    except: return False

def encode_url_safe(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode()).decode()

def decode_url_safe(b64: str) -> str:
    return base64.urlsafe_b64decode(b64).decode()

def encode_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode()

def size_ratio(text: str) -> float:
    enc = base64.b64encode(text.encode())
    return round(len(enc) / max(len(text.encode()), 1), 2)

def format_result_markdown(r: Base64Result) -> str:
    if not r.is_valid: return f"## Base64 ❌\n**Error:** {r.error}"
    return f"## Base64 ✅\n**Original:** {r.original_size}B → **Encoded:** {r.encoded_size}B"
