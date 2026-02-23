"""Phishing email detector — analyze emails for phishing indicators."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

SUSPICIOUS_PHRASES = [
    "verify your account", "click here immediately", "your account has been compromised",
    "act now", "limited time offer", "you have won", "claim your prize",
    "urgent action required", "confirm your identity", "suspended your account",
    "unusual activity", "reset your password", "dear customer", "dear user",
    "wire transfer", "western union", "bitcoin payment", "gift card",
    "social security number", "bank account details", "login credentials",
]

SUSPICIOUS_DOMAINS = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "is.gd", "buff.ly", "ow.ly"]

@dataclass
class PhishingResult:
    risk_score: int = 0  # 0-100
    risk_level: str = "low"  # low, medium, high, critical
    indicators: list[str] = field(default_factory=list)
    urls_found: list[str] = field(default_factory=list)
    suspicious_phrases_found: list[str] = field(default_factory=list)
    has_urgency: bool = False
    has_suspicious_links: bool = False
    has_personal_info_request: bool = False
    def to_dict(self) -> dict:
        return {"risk_score": self.risk_score, "risk_level": self.risk_level, "indicators": self.indicators, "urls": len(self.urls_found)}

def analyze_email(subject: str, body: str, sender: str = "") -> PhishingResult:
    r = PhishingResult()
    text = f"{subject} {body}".lower()
    # Check suspicious phrases
    for phrase in SUSPICIOUS_PHRASES:
        if phrase in text:
            r.suspicious_phrases_found.append(phrase)
    if r.suspicious_phrases_found:
        r.risk_score += min(40, len(r.suspicious_phrases_found) * 10)
        r.indicators.append(f"Suspicious phrases: {len(r.suspicious_phrases_found)}")
    # Check urgency
    urgency_words = ["urgent", "immediately", "act now", "expires", "deadline", "last chance", "final warning"]
    if any(w in text for w in urgency_words):
        r.has_urgency = True
        r.risk_score += 15
        r.indicators.append("High urgency language detected")
    # Check URLs
    r.urls_found = re.findall(r"https?://[^\s<>\"']+", body)
    for url in r.urls_found:
        domain = re.search(r"https?://([^/]+)", url)
        if domain and any(sd in domain.group(1) for sd in SUSPICIOUS_DOMAINS):
            r.has_suspicious_links = True
            r.risk_score += 20
            r.indicators.append(f"Shortened URL: {url[:50]}")
            break
    # Check personal info requests
    pii = ["password", "credit card", "ssn", "social security", "bank account", "login"]
    if any(p in text for p in pii):
        r.has_personal_info_request = True
        r.risk_score += 20
        r.indicators.append("Requests personal/financial information")
    # Sender analysis
    if sender:
        if re.search(r"\d{5,}", sender): r.risk_score += 10; r.indicators.append("Sender has many numbers")
        if not re.search(r"@[\w.-]+\.\w{2,}", sender): r.risk_score += 10; r.indicators.append("Invalid sender format")
    # Caps abuse
    caps_count = sum(1 for c in subject if c.isupper())
    if len(subject) > 5 and caps_count / max(len(subject), 1) > 0.6:
        r.risk_score += 10
        r.indicators.append("Excessive capitalization in subject")
    r.risk_score = min(100, r.risk_score)
    if r.risk_score >= 70: r.risk_level = "critical"
    elif r.risk_score >= 45: r.risk_level = "high"
    elif r.risk_score >= 20: r.risk_level = "medium"
    else: r.risk_level = "low"
    return r

def format_result_markdown(r: PhishingResult) -> str:
    emoji = {"low": "✅", "medium": "⚠️", "high": "🟠", "critical": "🔴"}.get(r.risk_level, "⬜")
    lines = [f"## Phishing Analysis {emoji}", f"**Risk Score:** {r.risk_score}/100 | **Level:** {r.risk_level}", ""]
    if r.indicators:
        lines.append("### Indicators")
        for i in r.indicators: lines.append(f"- 🚩 {i}")
    else:
        lines.append("✅ No phishing indicators detected")
    return "\n".join(lines)
