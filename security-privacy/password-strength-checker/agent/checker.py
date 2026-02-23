"""Password strength checker — analyze password security with entropy and suggestions."""
from __future__ import annotations
import re, math, string
from dataclasses import dataclass, field

@dataclass
class PasswordResult:
    password: str = ""; length: int = 0; entropy: float = 0; score: int = 0
    strength: str = ""; issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list); has_upper: bool = False
    has_lower: bool = False; has_digit: bool = False; has_special: bool = False
    def to_dict(self) -> dict: return {"length": self.length, "score": self.score, "strength": self.strength, "entropy": round(self.entropy, 1)}

COMMON_PASSWORDS = {"password", "123456", "qwerty", "admin", "letmein", "welcome", "monkey", "dragon", "master", "abc123", "password1", "iloveyou"}

def calculate_entropy(password: str) -> float:
    charset = 0
    if any(c in string.ascii_lowercase for c in password): charset += 26
    if any(c in string.ascii_uppercase for c in password): charset += 26
    if any(c in string.digits for c in password): charset += 10
    if any(c in string.punctuation for c in password): charset += 32
    if charset == 0: return 0
    return len(password) * math.log2(charset)

def check_password(password: str) -> PasswordResult:
    r = PasswordResult(password="*" * len(password), length=len(password))
    r.has_upper = bool(re.search(r'[A-Z]', password))
    r.has_lower = bool(re.search(r'[a-z]', password))
    r.has_digit = bool(re.search(r'\d', password))
    r.has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    r.entropy = calculate_entropy(password)
    # Score
    score = 0
    if r.length >= 8: score += 1
    if r.length >= 12: score += 1
    if r.has_upper: score += 1
    if r.has_lower: score += 1
    if r.has_digit: score += 1
    if r.has_special: score += 1
    if r.entropy > 50: score += 1
    if r.length >= 16: score += 1
    r.score = min(score, 10)
    # Issues
    if r.length < 8: r.issues.append("Too short (min 8 characters)")
    if not r.has_upper: r.issues.append("No uppercase letters")
    if not r.has_lower: r.issues.append("No lowercase letters")
    if not r.has_digit: r.issues.append("No digits")
    if not r.has_special: r.issues.append("No special characters")
    if password.lower() in COMMON_PASSWORDS: r.issues.append("Common password")
    if re.search(r'(.)\1{2,}', password): r.issues.append("Repeated characters")
    # Suggestions
    if r.score < 4: r.suggestions.append("Add more character types")
    if r.length < 12: r.suggestions.append("Use at least 12 characters")
    if not r.has_special: r.suggestions.append("Include symbols like !@#$%")
    # Strength label
    if r.score <= 2: r.strength = "weak"
    elif r.score <= 4: r.strength = "fair"
    elif r.score <= 6: r.strength = "good"
    else: r.strength = "strong"
    return r

def generate_policy_check(password: str, min_length: int = 8, require_upper: bool = True, require_digit: bool = True, require_special: bool = True) -> list[str]:
    fails = []
    if len(password) < min_length: fails.append(f"Min length {min_length}")
    if require_upper and not re.search(r'[A-Z]', password): fails.append("Uppercase required")
    if require_digit and not re.search(r'\d', password): fails.append("Digit required")
    if require_special and not re.search(r'[!@#$%^&*]', password): fails.append("Special char required")
    return fails

def format_result_markdown(r: PasswordResult) -> str:
    icons = {"weak": "🔴", "fair": "🟡", "good": "🟢", "strong": "💪"}
    emoji = icons.get(r.strength, "")
    lines = [f"## Password Check {emoji}", f"**Strength:** {r.strength} | **Score:** {r.score}/8 | **Entropy:** {r.entropy:.1f} bits", ""]
    if r.issues:
        lines.append("### Issues")
        for i in r.issues: lines.append(f"- ❌ {i}")
    if r.suggestions:
        lines.append("\n### Suggestions")
        for s in r.suggestions: lines.append(f"- 💡 {s}")
    return "\n".join(lines)
