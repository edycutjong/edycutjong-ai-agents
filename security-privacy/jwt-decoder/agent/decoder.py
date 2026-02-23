"""JWT decoder — decode and inspect JSON Web Tokens (without verification)."""
from __future__ import annotations
import base64, json
from dataclasses import dataclass
from datetime import datetime

@dataclass
class JWTResult:
    token: str = ""; header: dict = None; payload: dict = None; is_valid: bool = True
    is_expired: bool = False; error: str = ""; algorithm: str = ""
    def to_dict(self) -> dict: return {"algorithm": self.algorithm, "is_valid": self.is_valid, "is_expired": self.is_expired}

def _b64_decode(data: str) -> str:
    padding = 4 - len(data) % 4
    if padding != 4: data += "=" * padding
    return base64.urlsafe_b64decode(data).decode()

def decode_jwt(token: str) -> JWTResult:
    r = JWTResult(token=token)
    try:
        parts = token.split(".")
        if len(parts) != 3: r.is_valid = False; r.error = "Invalid JWT structure"; return r
        r.header = json.loads(_b64_decode(parts[0]))
        r.payload = json.loads(_b64_decode(parts[1]))
        r.algorithm = r.header.get("alg", "unknown")
        exp = r.payload.get("exp")
        if exp and isinstance(exp, (int, float)):
            r.is_expired = datetime.fromtimestamp(exp) < datetime.now()
    except Exception as e:
        r.is_valid = False; r.error = str(e)
    return r

def get_claims(token: str) -> dict:
    r = decode_jwt(token)
    return r.payload if r.payload else {}

def get_header(token: str) -> dict:
    r = decode_jwt(token)
    return r.header if r.header else {}

def is_expired(token: str) -> bool:
    return decode_jwt(token).is_expired

def _make_test_token(header: dict, payload: dict) -> str:
    h = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    p = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    return f"{h}.{p}.fakesignature"

def format_result_markdown(r: JWTResult) -> str:
    if not r.is_valid: return f"## JWT Decoder ❌\n**Error:** {r.error}"
    return f"## JWT Decoder 🔑\n**Algorithm:** {r.algorithm} | **Expired:** {r.is_expired}\n**Claims:** {json.dumps(r.payload, indent=2)[:200]}"
