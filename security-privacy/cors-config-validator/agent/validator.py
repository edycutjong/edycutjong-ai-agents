"""CORS config validator — check CORS headers for security best practices."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

@dataclass
class CorsConfig:
    allow_origins: list[str] = field(default_factory=list)
    allow_methods: list[str] = field(default_factory=list)
    allow_headers: list[str] = field(default_factory=list)
    allow_credentials: bool = False
    max_age: int = 0
    expose_headers: list[str] = field(default_factory=list)

@dataclass
class CorsResult:
    score: int = 100
    risk_level: str = "low"
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    def to_dict(self) -> dict:
        return {"score": self.score, "risk_level": self.risk_level, "issues": self.issues}

DANGEROUS_HEADERS = ["authorization", "x-api-key", "x-auth-token"]

def parse_cors_config(config: dict) -> CorsConfig:
    c = CorsConfig()
    c.allow_origins = config.get("allow_origins", config.get("Access-Control-Allow-Origin", [])) 
    if isinstance(c.allow_origins, str): c.allow_origins = [c.allow_origins]
    c.allow_methods = config.get("allow_methods", config.get("Access-Control-Allow-Methods", []))
    if isinstance(c.allow_methods, str): c.allow_methods = [m.strip() for m in c.allow_methods.split(",")]
    c.allow_headers = config.get("allow_headers", config.get("Access-Control-Allow-Headers", []))
    if isinstance(c.allow_headers, str): c.allow_headers = [h.strip() for h in c.allow_headers.split(",")]
    c.allow_credentials = config.get("allow_credentials", config.get("Access-Control-Allow-Credentials", False))
    if isinstance(c.allow_credentials, str): c.allow_credentials = c.allow_credentials.lower() == "true"
    c.max_age = int(config.get("max_age", config.get("Access-Control-Max-Age", 0)))
    return c

def validate_cors(config: CorsConfig) -> CorsResult:
    r = CorsResult()
    # Check wildcard origin
    if "*" in config.allow_origins:
        r.issues.append("Wildcard origin (*) allows any domain")
        r.score -= 30
        if config.allow_credentials:
            r.issues.append("CRITICAL: Wildcard origin with credentials is insecure")
            r.score -= 30
    # Check credentials
    if config.allow_credentials and not config.allow_origins:
        r.issues.append("Credentials enabled but no origins specified")
        r.score -= 15
    # Check methods
    if "*" in config.allow_methods:
        r.issues.append("Wildcard methods allows all HTTP methods")
        r.suggestions.append("Specify only needed methods: GET, POST, etc.")
        r.score -= 15
    dangerous_methods = [m for m in config.allow_methods if m.upper() in ("DELETE", "PATCH", "PUT")]
    if dangerous_methods:
        r.suggestions.append(f"Review if {', '.join(dangerous_methods)} methods are needed")
    # Check headers
    if "*" in config.allow_headers:
        r.issues.append("Wildcard headers allows any custom header")
        r.score -= 10
    for h in config.allow_headers:
        if h.lower() in DANGEROUS_HEADERS:
            r.suggestions.append(f"Sensitive header '{h}' is exposed via CORS")
    # Max-age
    if config.max_age > 86400:
        r.suggestions.append(f"Max-age {config.max_age}s may be too long (>24h)")
    # Risk level
    r.score = max(0, r.score)
    if r.score >= 80: r.risk_level = "low"
    elif r.score >= 50: r.risk_level = "medium"
    elif r.score >= 25: r.risk_level = "high"
    else: r.risk_level = "critical"
    return r

def format_result_markdown(config: CorsConfig, result: CorsResult) -> str:
    emoji = {"low": "✅", "medium": "⚠️", "high": "🟠", "critical": "🔴"}.get(result.risk_level, "⬜")
    lines = [f"## CORS Validation {emoji}", f"**Score:** {result.score}/100 | **Risk:** {result.risk_level}", ""]
    lines.append(f"**Origins:** {', '.join(config.allow_origins) or 'none'}")
    lines.append(f"**Methods:** {', '.join(config.allow_methods) or 'none'}")
    lines.append(f"**Credentials:** {config.allow_credentials}")
    if result.issues:
        lines.append("\n### Issues")
        for i in result.issues: lines.append(f"- ❌ {i}")
    if result.suggestions:
        lines.append("\n### Suggestions")
        for s in result.suggestions: lines.append(f"- 💡 {s}")
    return "\n".join(lines)
