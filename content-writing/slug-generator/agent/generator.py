"""Slug generator — convert text to URL-friendly slugs with customization."""
from __future__ import annotations
import re, unicodedata
from dataclasses import dataclass

TRANSLITERATIONS = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "ñ": "n", "ç": "c", "å": "a", "ø": "o", "æ": "ae"}

@dataclass
class SlugResult:
    original: str = ""; slug: str = ""; separator: str = "-"
    truncated: bool = False; max_length: int = 0
    def to_dict(self) -> dict: return {"original": self.original, "slug": self.slug, "truncated": self.truncated}

def slugify(text: str, separator: str = "-", max_length: int = 0, lowercase: bool = True) -> SlugResult:
    r = SlugResult(original=text, separator=separator, max_length=max_length)
    s = text
    for char, repl in TRANSLITERATIONS.items(): s = s.replace(char, repl)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    if lowercase: s = s.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', separator, s).strip(separator)
    s = re.sub(f'{re.escape(separator)}+', separator, s)
    if max_length and len(s) > max_length:
        s = s[:max_length].rstrip(separator)
        r.truncated = True
    r.slug = s
    return r

def batch_slugify(texts: list[str], **kwargs) -> list[SlugResult]:
    results = [slugify(t, **kwargs) for t in texts]
    seen = {}
    for r in results:
        if r.slug in seen:
            seen[r.slug] += 1
            r.slug = f"{r.slug}{kwargs.get('separator', '-')}{seen[r.slug]}"
        else: seen[r.slug] = 0
    return results

def is_valid_slug(slug: str) -> bool:
    return bool(re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', slug))

def format_result_markdown(r: SlugResult) -> str:
    lines = [f"## Slug Generator", f"**Original:** {r.original}", f"**Slug:** `{r.slug}`"]
    if r.truncated: lines.append(f"⚠️ Truncated to {r.max_length} chars")
    return "\n".join(lines)
