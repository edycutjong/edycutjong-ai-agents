"""HTTP header analyzer — analyze HTTP headers for security and best practices."""
from __future__ import annotations
from dataclasses import dataclass, field

SECURITY_HEADERS = {
    "Strict-Transport-Security": {"required": True, "desc": "Forces HTTPS connections"},
    "Content-Security-Policy": {"required": True, "desc": "Prevents XSS and injection attacks"},
    "X-Content-Type-Options": {"required": True, "desc": "Prevents MIME-type sniffing", "expected": "nosniff"},
    "X-Frame-Options": {"required": True, "desc": "Prevents clickjacking", "expected": ["DENY", "SAMEORIGIN"]},
    "X-XSS-Protection": {"required": False, "desc": "Legacy XSS protection"},
    "Referrer-Policy": {"required": True, "desc": "Controls referrer information"},
    "Permissions-Policy": {"required": False, "desc": "Controls browser features"},
    "Cache-Control": {"required": False, "desc": "Controls caching behavior"},
}

@dataclass
class HeaderResult:
    score: int = 100
    grade: str = "A"
    present: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    def to_dict(self) -> dict:
        return {"score": self.score, "grade": self.grade, "present": len(self.present), "missing": len(self.missing)}

def analyze_headers(headers: dict) -> HeaderResult:
    r = HeaderResult()
    norm = {k.lower(): v for k, v in headers.items()}
    for header, info in SECURITY_HEADERS.items():
        key = header.lower()
        if key in norm:
            r.present.append(header)
            if "expected" in info:
                val = norm[key]
                expected = info["expected"]
                if isinstance(expected, list):
                    if val not in expected:
                        r.issues.append(f"{header}: unexpected value '{val}' (expected {expected})")
                        r.score -= 5
                elif val != expected:
                    r.issues.append(f"{header}: expected '{expected}', got '{val}'")
                    r.score -= 5
        else:
            r.missing.append(header)
            if info.get("required"):
                r.score -= 15
                r.suggestions.append(f"Add {header}: {info['desc']}")
    info_headers = ["Server", "X-Powered-By", "X-AspNet-Version"]
    for h in info_headers:
        if h.lower() in norm:
            r.issues.append(f"{h} header reveals server info: {norm[h.lower()]}")
            r.score -= 5
    r.score = max(0, r.score)
    if r.score >= 90: r.grade = "A"
    elif r.score >= 75: r.grade = "B"
    elif r.score >= 60: r.grade = "C"
    elif r.score >= 40: r.grade = "D"
    else: r.grade = "F"
    return r

def format_result_markdown(r: HeaderResult) -> str:
    emoji = {"A": "🟢", "B": "🟡", "C": "🟠", "D": "🔴", "F": "💀"}.get(r.grade, "⬜")
    lines = [f"## HTTP Header Analysis {emoji}", f"**Score:** {r.score}/100 | **Grade:** {r.grade}", ""]
    if r.present:
        lines.append(f"### Present ({len(r.present)})")
        for h in r.present: lines.append(f"- ✅ {h}")
    if r.missing:
        lines.append(f"\n### Missing ({len(r.missing)})")
        for h in r.missing: lines.append(f"- ❌ {h}")
    if r.issues:
        lines.append(f"\n### Issues")
        for i in r.issues: lines.append(f"- ⚠️ {i}")
    return "\n".join(lines)
