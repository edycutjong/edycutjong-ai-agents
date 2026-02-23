"""Competitive analysis engine — compare products, features, and positioning."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Competitor:
    name: str
    description: str = ""
    website: str = ""
    pricing: str = ""
    target_market: str = ""
    features: list[str] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    differentiators: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v}

    @classmethod
    def from_dict(cls, data: dict) -> "Competitor":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class AnalysisReport:
    your_product: Competitor
    competitors: list[Competitor] = field(default_factory=list)
    feature_matrix: dict = field(default_factory=dict)
    market_gaps: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "your_product": self.your_product.to_dict(),
            "competitors": [c.to_dict() for c in self.competitors],
            "feature_matrix": self.feature_matrix,
            "market_gaps": self.market_gaps,
            "recommendations": self.recommendations,
        }


def build_feature_matrix(your_product: Competitor, competitors: list[Competitor]) -> dict:
    """Build a feature comparison matrix."""
    all_features = set(your_product.features)
    for c in competitors:
        all_features.update(c.features)

    matrix = {}
    for feature in sorted(all_features):
        matrix[feature] = {"your_product": feature in your_product.features}
        for c in competitors:
            matrix[feature][c.name] = feature in c.features

    return matrix


def find_market_gaps(your_product: Competitor, competitors: list[Competitor]) -> list[str]:
    """Find features competitors have that you don't."""
    your_features = set(f.lower() for f in your_product.features)
    gaps = []
    feature_count = defaultdict(int)

    for c in competitors:
        for f in c.features:
            if f.lower() not in your_features:
                feature_count[f] += 1

    for f, count in sorted(feature_count.items(), key=lambda x: -x[1]):
        pct = count / max(len(competitors), 1) * 100
        if pct >= 50:
            gaps.append(f"{f} (offered by {count}/{len(competitors)} competitors — {pct:.0f}%)")
        elif count >= 2:
            gaps.append(f"{f} (offered by {count} competitors)")

    return gaps


def find_unique_advantages(your_product: Competitor, competitors: list[Competitor]) -> list[str]:
    """Find features only you have."""
    competitor_features = set()
    for c in competitors:
        competitor_features.update(f.lower() for f in c.features)

    return [f for f in your_product.features if f.lower() not in competitor_features]


def score_competitor(competitor: Competitor) -> dict:
    """Score a competitor on multiple dimensions."""
    scores = {
        "feature_breadth": min(len(competitor.features) * 10, 100),
        "differentiation": min(len(competitor.differentiators) * 20, 100),
        "market_clarity": 80 if competitor.target_market else 30,
        "pricing_transparency": 80 if competitor.pricing else 20,
    }
    scores["overall"] = round(sum(scores.values()) / len(scores))
    return scores


def generate_recommendations(your_product: Competitor, competitors: list[Competitor]) -> list[str]:
    """Generate strategic recommendations."""
    recs = []
    gaps = find_market_gaps(your_product, competitors)
    unique = find_unique_advantages(your_product, competitors)

    if gaps:
        recs.append(f"🎯 Address {len(gaps)} feature gap(s) — especially: {gaps[0]}")
    if unique:
        recs.append(f"💎 Promote unique advantages: {', '.join(unique[:3])}")
    if len(competitors) >= 3:
        recs.append("📊 Market is competitive — focus on differentiation")
    if not your_product.differentiators:
        recs.append("⚡ Define clear differentiators to stand out")
    if not your_product.target_market:
        recs.append("🎯 Clarify your target market for focused positioning")

    return recs


def run_analysis(your_product: Competitor, competitors: list[Competitor]) -> AnalysisReport:
    """Run full competitive analysis."""
    return AnalysisReport(
        your_product=your_product,
        competitors=competitors,
        feature_matrix=build_feature_matrix(your_product, competitors),
        market_gaps=find_market_gaps(your_product, competitors),
        recommendations=generate_recommendations(your_product, competitors),
    )


def format_report_markdown(report: AnalysisReport) -> str:
    """Format competitive analysis as Markdown."""
    lines = [
        f"# Competitive Analysis: {report.your_product.name}",
        f"**vs** {', '.join(c.name for c in report.competitors)}",
        "",
    ]

    # Feature Matrix
    all_names = [report.your_product.name] + [c.name for c in report.competitors]
    lines.append("## Feature Matrix")
    lines.append("| Feature | " + " | ".join(all_names) + " |")
    lines.append("|---------|" + "|".join(["-------"] * len(all_names)) + "|")
    for feature, data in report.feature_matrix.items():
        row = [feature]
        row.append("✅" if data.get("your_product") else "❌")
        for c in report.competitors:
            row.append("✅" if data.get(c.name) else "❌")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # Unique Advantages
    unique = find_unique_advantages(report.your_product, report.competitors)
    if unique:
        lines.append("## 💎 Unique Advantages")
        for u in unique:
            lines.append(f"- {u}")
        lines.append("")

    # Gaps
    if report.market_gaps:
        lines.append("## 🔍 Market Gaps")
        for g in report.market_gaps:
            lines.append(f"- {g}")
        lines.append("")

    # Recommendations
    if report.recommendations:
        lines.append("## 📋 Recommendations")
        for r in report.recommendations:
            lines.append(f"- {r}")

    return "\n".join(lines)
