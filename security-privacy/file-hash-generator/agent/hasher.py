"""File hash generator — compute cryptographic hashes for data integrity."""
from __future__ import annotations
import hashlib
from dataclasses import dataclass

ALGORITHMS = ["md5", "sha1", "sha256", "sha384", "sha512", "sha3_256"]

@dataclass
class HashResult:
    data_size: int = 0; hashes: dict = None; primary: str = ""; algorithm: str = "sha256"
    def __post_init__(self):
        if self.hashes is None: self.hashes = {}
    def to_dict(self) -> dict: return {"size": self.data_size, "sha256": self.hashes.get("sha256", ""), "algorithm": self.algorithm}

def hash_text(text: str, algorithm: str = "sha256") -> HashResult:
    data = text.encode()
    r = HashResult(data_size=len(data), algorithm=algorithm)
    for algo in ALGORITHMS:
        h = hashlib.new(algo)
        h.update(data)
        r.hashes[algo] = h.hexdigest()
    r.primary = r.hashes.get(algorithm, "")
    return r

def hash_bytes(data: bytes, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm); h.update(data); return h.hexdigest()

def verify_hash(text: str, expected: str, algorithm: str = "sha256") -> bool:
    return hash_bytes(text.encode(), algorithm) == expected.lower()

def compare_hashes(text1: str, text2: str, algorithm: str = "sha256") -> bool:
    return hash_bytes(text1.encode(), algorithm) == hash_bytes(text2.encode(), algorithm)

def checksum(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:8]

def format_result_markdown(r: HashResult) -> str:
    lines = [f"## Hash Generator 🔒", f"**Size:** {r.data_size}B | **Algorithm:** {r.algorithm}", ""]
    for algo, val in r.hashes.items(): lines.append(f"- **{algo}:** `{val[:20]}...`")
    return "\n".join(lines)
