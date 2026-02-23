"""Core cost calculator — computes costs, generates reports, forecasts spending."""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict
from agent.pricing import PRICING, get_model_price


@dataclass
class UsageEntry:
    """A single API usage record."""
    model: str
    input_tokens: int
    output_tokens: int
    timestamp: str  # ISO format
    label: str = ""  # optional tag like "summarization", "chat"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "UsageEntry":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> dict:
    """Calculate cost for a single API call.

    Returns:
        dict with input_cost, output_cost, total_cost (all in USD).
    """
    price = get_model_price(model)
    if not price:
        return {"error": f"Unknown model: {model}", "total_cost": 0.0}

    input_cost = (input_tokens / 1_000_000) * price["input"]
    output_cost = (output_tokens / 1_000_000) * price["output"]
    total = input_cost + output_cost

    return {
        "model": model,
        "provider": price["provider"],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(total, 6),
    }


def generate_cost_report(entries: list[UsageEntry]) -> dict:
    """Generate a comprehensive cost breakdown report from usage entries.

    Returns:
        dict with total_cost, by_model, by_provider, by_label, high_cost_queries.
    """
    total_cost = 0.0
    total_input = 0
    total_output = 0
    by_model = defaultdict(lambda: {"cost": 0.0, "calls": 0, "input_tokens": 0, "output_tokens": 0})
    by_provider = defaultdict(lambda: {"cost": 0.0, "calls": 0})
    by_label = defaultdict(lambda: {"cost": 0.0, "calls": 0})
    all_costs = []

    for entry in entries:
        result = calculate_cost(entry.model, entry.input_tokens, entry.output_tokens)
        cost = result["total_cost"]
        provider = result.get("provider", "Unknown")

        total_cost += cost
        total_input += entry.input_tokens
        total_output += entry.output_tokens

        by_model[entry.model]["cost"] += cost
        by_model[entry.model]["calls"] += 1
        by_model[entry.model]["input_tokens"] += entry.input_tokens
        by_model[entry.model]["output_tokens"] += entry.output_tokens

        by_provider[provider]["cost"] += cost
        by_provider[provider]["calls"] += 1

        label = entry.label or "unlabeled"
        by_label[label]["cost"] += cost
        by_label[label]["calls"] += 1

        all_costs.append({"entry": entry.to_dict(), "cost": cost})

    # Round all costs
    for m in by_model.values():
        m["cost"] = round(m["cost"], 6)
    for p in by_provider.values():
        p["cost"] = round(p["cost"], 6)
    for l in by_label.values():
        l["cost"] = round(l["cost"], 6)

    # Find high-cost queries (top 5)
    all_costs.sort(key=lambda x: x["cost"], reverse=True)
    high_cost = all_costs[:5]

    return {
        "total_cost": round(total_cost, 6),
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_calls": len(entries),
        "by_model": dict(by_model),
        "by_provider": dict(by_provider),
        "by_label": dict(by_label),
        "high_cost_queries": high_cost,
    }


def forecast_monthly_cost(entries: list[UsageEntry], days_in_window: int = 7) -> dict:
    """Forecast monthly cost based on recent usage.

    Args:
        entries: Usage entries.
        days_in_window: Number of days the entries span.

    Returns:
        dict with daily_avg, weekly_projection, monthly_projection.
    """
    if not entries or days_in_window <= 0:
        return {"daily_avg": 0.0, "weekly_projection": 0.0, "monthly_projection": 0.0}

    total = 0.0
    for entry in entries:
        result = calculate_cost(entry.model, entry.input_tokens, entry.output_tokens)
        total += result["total_cost"]

    daily_avg = total / days_in_window
    return {
        "daily_avg": round(daily_avg, 4),
        "weekly_projection": round(daily_avg * 7, 4),
        "monthly_projection": round(daily_avg * 30, 4),
        "total_in_window": round(total, 4),
        "days_in_window": days_in_window,
    }


def check_budget(entries: list[UsageEntry], budget: float) -> dict:
    """Check if current spend is within budget.

    Args:
        entries: Usage entries.
        budget: Monthly budget in USD.

    Returns:
        dict with spend, budget, remaining, over_budget, usage_percent.
    """
    total = 0.0
    for entry in entries:
        result = calculate_cost(entry.model, entry.input_tokens, entry.output_tokens)
        total += result["total_cost"]

    remaining = budget - total
    return {
        "spend": round(total, 4),
        "budget": budget,
        "remaining": round(remaining, 4),
        "over_budget": total > budget,
        "usage_percent": round((total / budget) * 100, 1) if budget > 0 else 0.0,
    }


def format_report_markdown(report: dict) -> str:
    """Format a cost report as readable Markdown."""
    lines = [
        "# LLM Cost Report",
        "",
        f"**Total Cost:** ${report['total_cost']:.4f}",
        f"**Total Calls:** {report['total_calls']}",
        f"**Input Tokens:** {report['total_input_tokens']:,}",
        f"**Output Tokens:** {report['total_output_tokens']:,}",
        "",
    ]

    # By Model
    lines.append("## Cost by Model")
    lines.append("| Model | Calls | Input Tokens | Output Tokens | Cost |")
    lines.append("|-------|-------|-------------|--------------|------|")
    for model, data in sorted(report["by_model"].items(), key=lambda x: x[1]["cost"], reverse=True):
        lines.append(
            f"| {model} | {data['calls']} | {data['input_tokens']:,} | {data['output_tokens']:,} | ${data['cost']:.4f} |"
        )
    lines.append("")

    # By Provider
    lines.append("## Cost by Provider")
    lines.append("| Provider | Calls | Cost |")
    lines.append("|----------|-------|------|")
    for provider, data in sorted(report["by_provider"].items(), key=lambda x: x[1]["cost"], reverse=True):
        lines.append(f"| {provider} | {data['calls']} | ${data['cost']:.4f} |")
    lines.append("")

    # High Cost
    if report.get("high_cost_queries"):
        lines.append("## Top 5 Most Expensive Calls")
        for i, item in enumerate(report["high_cost_queries"], 1):
            entry = item["entry"]
            lines.append(f"{i}. **{entry['model']}** — ${item['cost']:.6f} ({entry['input_tokens']:,} in / {entry['output_tokens']:,} out)")
        lines.append("")

    return "\n".join(lines)
