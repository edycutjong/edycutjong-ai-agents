"""Password strength analyzer — evaluate password security with scoring."""
from __future__ import annotations
import re, math, string
from dataclasses import dataclass

@dataclass
class PasswordResult:
    password: str = ""
    score: int = 0  # 0-100
    strength: str = "weak"  # weak, fair, good, strong, very_strong
    length: int = 0
    has_upper: bool = False
    has_lower: bool = False
    has_digit: bool = False
    has_special: bool = False
    entropy: float = 0.0
    issues: list = None
    suggestions: list = None
    def __post_init__(self):
        if self.issues is None: self.issues = []
        if self.suggestions is None: self.suggestions = []
    def to_dict(self) -> dict:
        return {"score": self.score, "strength": self.strength, "length": self.length, "entropy": round(self.entropy, 1), "issues": self.issues, "suggestions": self.suggestions}

COMMON_PASSWORDS = {"password", "123456", "12345678", "qwerty", "abc123", "monkey", "1234567", "letmein", "trustno1", "dragon", "baseball", "iloveyou", "master", "sunshine", "ashley", "bailey", "passw0rd", "shadow", "123123", "654321", "superman", "qazwsx", "michael", "football", "password1", "password123", "admin", "welcome", "hello123"}

def calculate_entropy(password: str) -> float:
    charset = 0
    if any(c in string.ascii_lowercase for c in password): charset += 26
    if any(c in string.ascii_uppercase for c in password): charset += 26
    if any(c in string.digits for c in password): charset += 10
    if any(c in string.punctuation for c in password): charset += 32
    if charset == 0: return 0
    return len(password) * math.log2(charset)

def analyze_password(password: str) -> PasswordResult:
    r = PasswordResult(password="*" * len(password), length=len(password))
    r.has_upper = bool(re.search(r"[A-Z]", password))
    r.has_lower = bool(re.search(r"[a-z]", password))
    r.has_digit = bool(re.search(r"\d", password))
    r.has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\;'/`~]", password))
    r.entropy = calculate_entropy(password)
    # Score
    score = 0
    if r.length >= 8: score += 15
    if r.length >= 12: score += 15
    if r.length >= 16: score += 10
    if r.has_upper: score += 10
    if r.has_lower: score += 10
    if r.has_digit: score += 10
    if r.has_special: score += 15
    if r.entropy > 50: score += 10
    if r.entropy > 70: score += 5
    # Deductions
    if password.lower() in COMMON_PASSWORDS:
        score = max(0, score - 50)
        r.issues.append("Common password detected")
    if re.search(r"(.)\1{2,}", password):
        score -= 10
        r.issues.append("Repeated characters detected")
    if re.search(r"(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)", password.lower()):
        score -= 10
        r.issues.append("Sequential characters detected")
    r.score = max(0, min(100, score))
    # Strength label
    if r.score >= 80: r.strength = "very_strong"
    elif r.score >= 60: r.strength = "strong"
    elif r.score >= 40: r.strength = "good"
    elif r.score >= 20: r.strength = "fair"
    else: r.strength = "weak"
    # Suggestions
    if r.length < 12: r.suggestions.append("Use at least 12 characters")
    if not r.has_upper: r.suggestions.append("Add uppercase letters")
    if not r.has_lower: r.suggestions.append("Add lowercase letters")
    if not r.has_digit: r.suggestions.append("Add numbers")
    if not r.has_special: r.suggestions.append("Add special characters")
    return r

def format_result_markdown(r: PasswordResult) -> str:
    emoji = {"weak": "🔴", "fair": "🟠", "good": "🟡", "strong": "🟢", "very_strong": "💪"}.get(r.strength, "⬜")
    lines = [f"## Password Analysis {emoji}", f"**Score:** {r.score}/100 | **Strength:** {r.strength} | **Length:** {r.length} | **Entropy:** {r.entropy:.1f} bits", ""]
    checks = [("Uppercase", r.has_upper), ("Lowercase", r.has_lower), ("Digits", r.has_digit), ("Special", r.has_special)]
    for name, ok in checks: lines.append(f"{'✅' if ok else '❌'} {name}")
    if r.issues:
        lines.append("\n### Issues")
        for i in r.issues: lines.append(f"- ⚠️ {i}")
    if r.suggestions:
        lines.append("\n### Suggestions")
        for s in r.suggestions: lines.append(f"- 💡 {s}")
    return "\n".join(lines)
