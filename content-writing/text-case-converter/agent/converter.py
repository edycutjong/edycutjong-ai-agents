"""Text case converter — convert text between various cases."""
from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass
class CaseResult:
    original: str = ""; converted: str = ""; target_case: str = ""
    def to_dict(self) -> dict: return {"original": self.original, "converted": self.converted, "case": self.target_case}

def _split_words(text: str) -> list[str]:
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'[-_./\\]', ' ', text)
    return [w for w in text.split() if w]

def to_camel(text: str) -> CaseResult:
    words = _split_words(text)
    r = words[0].lower() + "".join(w.capitalize() for w in words[1:]) if words else ""
    return CaseResult(original=text, converted=r, target_case="camelCase")

def to_pascal(text: str) -> CaseResult:
    words = _split_words(text)
    r = "".join(w.capitalize() for w in words) if words else ""
    return CaseResult(original=text, converted=r, target_case="PascalCase")

def to_snake(text: str) -> CaseResult:
    words = _split_words(text)
    r = "_".join(w.lower() for w in words) if words else ""
    return CaseResult(original=text, converted=r, target_case="snake_case")

def to_kebab(text: str) -> CaseResult:
    words = _split_words(text)
    r = "-".join(w.lower() for w in words) if words else ""
    return CaseResult(original=text, converted=r, target_case="kebab-case")

def to_constant(text: str) -> CaseResult:
    words = _split_words(text)
    r = "_".join(w.upper() for w in words) if words else ""
    return CaseResult(original=text, converted=r, target_case="CONSTANT_CASE")

def to_title(text: str) -> CaseResult:
    words = _split_words(text)
    r = " ".join(w.capitalize() for w in words) if words else ""
    return CaseResult(original=text, converted=r, target_case="Title Case")

def to_sentence(text: str) -> CaseResult:
    words = _split_words(text)
    if not words: return CaseResult(original=text, converted="", target_case="Sentence case")
    r = words[0].capitalize() + " " + " ".join(w.lower() for w in words[1:]) if len(words) > 1 else words[0].capitalize()
    return CaseResult(original=text, converted=r, target_case="Sentence case")

def detect_case(text: str) -> str:
    if "_" in text and text == text.upper(): return "CONSTANT_CASE"
    if "_" in text: return "snake_case"
    if "-" in text: return "kebab-case"
    if text[0].islower() and any(c.isupper() for c in text[1:]): return "camelCase"
    if text[0].isupper() and any(c.isupper() for c in text[1:]): return "PascalCase"
    return "unknown"

def convert_all(text: str) -> dict[str, str]:
    return {f.target_case: f.converted for f in [to_camel(text), to_pascal(text), to_snake(text), to_kebab(text), to_constant(text), to_title(text)]}

def format_result_markdown(r: CaseResult) -> str:
    return f"## Case Converter 🔤\n`{r.original}` → **`{r.converted}`** ({r.target_case})"
