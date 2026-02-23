"""Contract analysis engine — extract clauses, detect risks, and summarize agreements."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime


# Risk keywords with severity levels
RISK_PATTERNS = {
    "high": [
        r"unlimited\s+liability", r"indemnif(?:y|ication)", r"personal\s+guarantee",
        r"auto[\s-]?renew", r"automatic\s+renewal", r"non[\s-]?compete",
        r"exclusive\s+(?:rights|license)", r"irrevocable", r"perpetual\s+license",
        r"waive?\s+(?:right|claim)", r"liquidated\s+damages", r"penalty\s+clause",
    ],
    "medium": [
        r"confidential(?:ity)?", r"non[\s-]?disclosure", r"termination\s+fee",
        r"early\s+termination", r"governing\s+law", r"arbitration",
        r"force\s+majeure", r"assignment\s+(?:clause|rights)", r"warranty\s+disclaim",
        r"limitation\s+of\s+liability",
    ],
    "low": [
        r"notice\s+period", r"amendment", r"entire\s+agreement",
        r"severability", r"counterpart", r"headings?\s+for\s+convenience",
    ],
}

# Common clause types
CLAUSE_PATTERNS = {
    "Payment Terms": [r"payment\s+terms?", r"net\s+\d+", r"due\s+(?:within|upon)", r"invoice"],
    "Termination": [r"terminat(?:e|ion)", r"cancel(?:lation)?", r"end\s+of\s+(?:term|agreement)"],
    "Confidentiality": [r"confidential", r"non[\s-]?disclosure", r"NDA", r"trade\s+secret"],
    "Liability": [r"liabilit(?:y|ies)", r"indemnif", r"hold\s+harmless", r"damages?"],
    "Intellectual Property": [r"intellectual\s+property", r"copyright", r"patent", r"trademark", r"IP\s+rights"],
    "Warranties": [r"warrant(?:y|ies)", r"represent(?:s|ation)", r"as[\s-]?is", r"disclaim"],
    "Dispute Resolution": [r"dispute", r"arbitration", r"mediation", r"litigation", r"governing\s+law"],
    "Non-Compete": [r"non[\s-]?compete", r"restrictive\s+covenant", r"non[\s-]?solicitation"],
    "Data Privacy": [r"data\s+(?:privacy|protection)", r"GDPR", r"personal\s+(?:data|information)", r"CCPA"],
}


@dataclass
class ContractClause:
    """An identified clause in a contract."""
    clause_type: str
    text_snippet: str
    position: int  # approximate character position
    confidence: float = 1.0

    def to_dict(self) -> dict:
        return {"type": self.clause_type, "snippet": self.text_snippet[:200],
                "position": self.position, "confidence": self.confidence}


@dataclass
class RiskItem:
    """A detected risk in a contract."""
    severity: str  # high, medium, low
    description: str
    snippet: str
    recommendation: str = ""

    def to_dict(self) -> dict:
        return {"severity": self.severity, "description": self.description,
                "snippet": self.snippet[:200], "recommendation": self.recommendation}


@dataclass
class AnalysisResult:
    """Result of contract analysis."""
    clauses: list[ContractClause] = field(default_factory=list)
    risks: list[RiskItem] = field(default_factory=list)
    parties: list[str] = field(default_factory=list)
    dates: list[str] = field(default_factory=list)
    word_count: int = 0
    estimated_read_time: int = 0  # minutes

    @property
    def high_risks(self) -> int:
        return sum(1 for r in self.risks if r.severity == "high")

    @property
    def risk_score(self) -> int:
        """0-100 risk score (higher = riskier)."""
        score = self.high_risks * 20 + sum(1 for r in self.risks if r.severity == "medium") * 8 + sum(1 for r in self.risks if r.severity == "low") * 3
        return min(score, 100)

    def to_dict(self) -> dict:
        return {
            "word_count": self.word_count,
            "estimated_read_time": self.estimated_read_time,
            "parties": self.parties,
            "dates": self.dates,
            "clauses": [c.to_dict() for c in self.clauses],
            "risks": [r.to_dict() for r in self.risks],
            "risk_score": self.risk_score,
            "high_risks": self.high_risks,
        }


RISK_RECOMMENDATIONS = {
    "unlimited liability": "Negotiate a liability cap based on contract value",
    "indemnif": "Review indemnification scope — ensure it's mutual and reasonable",
    "personal guarantee": "Avoid personal guarantees if possible — use corporate liability",
    "auto-renew": "Add clear opt-out mechanism before auto-renewal",
    "automatic renewal": "Add clear opt-out mechanism before auto-renewal",
    "non-compete": "Verify geographic and time scope are reasonable",
    "exclusive": "Consider whether exclusivity is necessary and appropriately scoped",
    "irrevocable": "Ensure irrevocable terms have clear boundaries",
    "perpetual license": "Negotiate time-limited license with renewal options",
    "waive": "Be cautious about waiving rights — may be unrecoverable",
    "liquidated damages": "Verify amounts are proportional to actual potential losses",
    "penalty clause": "Ensure penalties are enforceable in your jurisdiction",
}


def analyze_contract(text: str) -> AnalysisResult:
    """Perform comprehensive contract analysis."""
    result = AnalysisResult()
    result.word_count = len(text.split())
    result.estimated_read_time = max(1, result.word_count // 250)

    lower_text = text.lower()

    # Extract parties
    party_patterns = [
        r"(?:between|by and between)\s+[\"']?([A-Z][A-Za-z\s,\.]+?)(?=\"|\s+and\s+|\s+\()",
        r"(?:hereinafter|referred to as)\s+[\"']([^\"']+)[\"']",
    ]
    for pattern in party_patterns:
        matches = re.findall(pattern, text)
        result.parties.extend(m.strip() for m in matches if len(m.strip()) > 2)
    result.parties = list(dict.fromkeys(result.parties))[:10]

    # Extract dates
    date_patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
    ]
    for pattern in date_patterns:
        result.dates.extend(re.findall(pattern, text))
    result.dates = list(dict.fromkeys(result.dates))[:10]

    # Identify clauses
    for clause_type, patterns in CLAUSE_PATTERNS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, lower_text):
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 150)
                snippet = text[start:end].strip()
                result.clauses.append(ContractClause(
                    clause_type=clause_type, text_snippet=snippet, position=match.start(),
                ))
                break  # one match per clause type per pattern

    # Detect risks
    for severity, patterns in RISK_PATTERNS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, lower_text):
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 100)
                snippet = text[start:end].strip()

                rec = ""
                for key, recommendation in RISK_RECOMMENDATIONS.items():
                    if key in match.group().lower():
                        rec = recommendation
                        break

                result.risks.append(RiskItem(
                    severity=severity, description=f"Found: {match.group()}",
                    snippet=snippet, recommendation=rec,
                ))

    return result


def format_analysis_markdown(result: AnalysisResult) -> str:
    """Format analysis as Markdown."""
    bar = "█" * (result.risk_score // 10) + "░" * (10 - result.risk_score // 10)
    lines = [
        "# Contract Analysis Report",
        "",
        f"**Words:** {result.word_count:,} | **Read Time:** ~{result.estimated_read_time} min",
        f"**Risk Score:** {result.risk_score}/100 [{bar}]",
        "",
    ]

    if result.parties:
        lines.append(f"**Parties:** {', '.join(result.parties)}")
    if result.dates:
        lines.append(f"**Key Dates:** {', '.join(result.dates)}")

    if result.risks:
        lines.extend(["", "## ⚠️ Risk Items"])
        for r in sorted(result.risks, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x.severity]):
            emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[r.severity]
            lines.append(f"- {emoji} **[{r.severity.upper()}]** {r.description}")
            if r.recommendation:
                lines.append(f"  - 💡 {r.recommendation}")

    if result.clauses:
        lines.extend(["", "## 📋 Identified Clauses"])
        seen = set()
        for c in result.clauses:
            if c.clause_type not in seen:
                seen.add(c.clause_type)
                lines.append(f"- **{c.clause_type}**: _{c.text_snippet[:100]}..._")

    return "\n".join(lines)
