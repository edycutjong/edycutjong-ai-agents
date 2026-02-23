"""URL shortener — create short URL hashes and track mappings."""
from __future__ import annotations
import hashlib, string
from dataclasses import dataclass, field

BASE62 = string.ascii_letters + string.digits

@dataclass
class ShortURLResult:
    original: str = ""; short_code: str = ""; full_short: str = ""; is_valid: bool = True; error: str = ""
    def to_dict(self) -> dict: return {"original": self.original, "short_code": self.short_code}

class URLStore:
    def __init__(self): self._map: dict[str, str] = {}; self._reverse: dict[str, str] = {}
    def shorten(self, url: str, length: int = 6) -> ShortURLResult:
        if not url.startswith(("http://", "https://")): return ShortURLResult(original=url, is_valid=False, error="Invalid URL")
        if url in self._reverse: return ShortURLResult(original=url, short_code=self._reverse[url], full_short=f"https://short.ly/{self._reverse[url]}")
        code = _generate_code(url, length)
        while code in self._map: code = _generate_code(url + code, length)
        self._map[code] = url; self._reverse[url] = code
        return ShortURLResult(original=url, short_code=code, full_short=f"https://short.ly/{code}")
    def resolve(self, code: str) -> str: return self._map.get(code, "")
    def stats(self) -> dict: return {"total_urls": len(self._map)}

def _generate_code(url: str, length: int = 6) -> str:
    h = hashlib.sha256(url.encode()).hexdigest()
    num = int(h[:12], 16)
    chars = []
    while num and len(chars) < length:
        chars.append(BASE62[num % 62]); num //= 62
    return "".join(chars).ljust(length, "a")

def is_valid_url(url: str) -> bool:
    import re
    return bool(re.match(r'^https?://[^\s]+$', url))

def bulk_shorten(urls: list[str], store: URLStore = None) -> list[ShortURLResult]:
    if not store: store = URLStore()
    return [store.shorten(u) for u in urls]

def format_result_markdown(r: ShortURLResult) -> str:
    if not r.is_valid: return f"## URL Shortener ❌\n**Error:** {r.error}"
    return f"## URL Shortener 🔗\n`{r.original}` → **`{r.full_short}`**"
