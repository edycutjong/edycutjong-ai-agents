"""Hash generator — generate and verify cryptographic hashes."""
from __future__ import annotations
import hashlib
from dataclasses import dataclass

ALGORITHMS = {"md5": hashlib.md5, "sha1": hashlib.sha1, "sha256": hashlib.sha256, "sha512": hashlib.sha512, "sha3_256": hashlib.sha3_256}

@dataclass
class HashResult:
    input_text: str = ""; algorithm: str = ""; hash_value: str = ""; length: int = 0
    def to_dict(self) -> dict: return {"algorithm": self.algorithm, "hash": self.hash_value, "length": self.length}

def generate_hash(text: str, algorithm: str = "sha256") -> HashResult:
    algo = algorithm.lower().replace("-", "_")
    func = ALGORITHMS.get(algo)
    if not func: return HashResult(input_text=text, algorithm=algo)
    h = func(text.encode("utf-8")).hexdigest()
    return HashResult(input_text=text, algorithm=algo, hash_value=h, length=len(h))

def hash_file_bytes(data: bytes, algorithm: str = "sha256") -> str:
    func = ALGORITHMS.get(algorithm.lower().replace("-", "_"), hashlib.sha256)
    return func(data).hexdigest()

def verify_hash(text: str, expected: str, algorithm: str = "sha256") -> bool:
    r = generate_hash(text, algorithm)
    return r.hash_value == expected.lower()

def multi_hash(text: str) -> dict:
    return {algo: generate_hash(text, algo).hash_value for algo in ALGORITHMS}

def compare_hashes(hash_a: str, hash_b: str) -> bool:
    return hash_a.lower().strip() == hash_b.lower().strip()

def detect_algorithm(hash_value: str) -> str:
    length_map = {32: "md5", 40: "sha1", 64: "sha256", 128: "sha512"}
    return length_map.get(len(hash_value.strip()), "unknown")

def format_result_markdown(r: HashResult) -> str:
    return f"## Hash Generator 🔐\n**Algorithm:** {r.algorithm} | **Length:** {r.length}\n```\n{r.hash_value}\n```"
