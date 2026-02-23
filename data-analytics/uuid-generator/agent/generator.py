"""UUID generator — generate and validate UUIDs in multiple versions."""
from __future__ import annotations
import uuid
from dataclasses import dataclass

@dataclass
class UUIDResult:
    value: str = ""; version: int = 0; variant: str = ""; is_nil: bool = False
    def to_dict(self) -> dict: return {"uuid": self.value, "version": self.version, "variant": self.variant}

def generate_v1() -> UUIDResult:
    u = uuid.uuid1(); return UUIDResult(value=str(u), version=1, variant=str(u.variant))

def generate_v4() -> UUIDResult:
    u = uuid.uuid4(); return UUIDResult(value=str(u), version=4, variant=str(u.variant))

def generate_v5(namespace: str, name: str) -> UUIDResult:
    ns = {"dns": uuid.NAMESPACE_DNS, "url": uuid.NAMESPACE_URL, "oid": uuid.NAMESPACE_OID}.get(namespace.lower(), uuid.NAMESPACE_DNS)
    u = uuid.uuid5(ns, name); return UUIDResult(value=str(u), version=5, variant=str(u.variant))

def generate_v3(namespace: str, name: str) -> UUIDResult:
    ns = {"dns": uuid.NAMESPACE_DNS, "url": uuid.NAMESPACE_URL}.get(namespace.lower(), uuid.NAMESPACE_DNS)
    u = uuid.uuid3(ns, name); return UUIDResult(value=str(u), version=3, variant=str(u.variant))

def validate_uuid(value: str) -> tuple[bool, int]:
    try:
        u = uuid.UUID(value)
        return True, u.version or 0
    except ValueError:
        return False, 0

def is_nil_uuid(value: str) -> bool:
    return value == "00000000-0000-0000-0000-000000000000"

def bulk_generate(count: int, version: int = 4) -> list[str]:
    funcs = {1: generate_v1, 4: generate_v4}
    gen = funcs.get(version, generate_v4)
    return [gen().value for _ in range(min(count, 1000))]

def parse_uuid(value: str) -> dict:
    try:
        u = uuid.UUID(value)
        return {"hex": u.hex, "int": u.int, "version": u.version, "variant": str(u.variant), "urn": u.urn}
    except: return {}

def format_result_markdown(r: UUIDResult) -> str:
    return f"## UUID Generator 🔑\n**Version:** {r.version} | **Value:** `{r.value}`"
