"""Model benchmark runner — compare LLM outputs with scoring metrics."""
from __future__ import annotations

import json, os, time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from config import Config


@dataclass
class BenchmarkCase:
    """A single test case for benchmarking."""
    prompt: str
    expected: str = ""
    category: str = "general"
    metadata: dict = field(default_factory=dict)


@dataclass
class ModelResult:
    """Result from a model on a single case."""
    model: str
    prompt: str
    output: str
    latency_ms: float = 0
    token_count: int = 0
    scores: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BenchmarkReport:
    """Full benchmark report comparing models."""
    name: str = ""
    timestamp: str = ""
    models: list[str] = field(default_factory=list)
    results: list[ModelResult] = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {"name": self.name, "timestamp": self.timestamp, "models": self.models,
                "results": [r.to_dict() for r in self.results], "summary": self.summary}


# --- Scoring Functions ---

def score_exact_match(output: str, expected: str) -> float:
    """1.0 if exact match, 0.0 otherwise."""
    return 1.0 if output.strip() == expected.strip() else 0.0


def score_contains(output: str, expected: str) -> float:
    """1.0 if output contains expected, 0.0 otherwise."""
    return 1.0 if expected.strip().lower() in output.strip().lower() else 0.0


def score_length_ratio(output: str, expected: str) -> float:
    """Score based on length similarity (0-1)."""
    if not expected:
        return 1.0 if output else 0.0
    ratio = len(output) / max(len(expected), 1)
    if 0.5 <= ratio <= 2.0:
        return 1.0 - abs(1.0 - ratio) * 0.5
    return max(0.0, 1.0 - abs(1.0 - ratio))


def score_keyword_coverage(output: str, expected: str) -> float:
    """Score based on keyword overlap."""
    if not expected:
        return 1.0
    expected_words = set(expected.lower().split())
    output_words = set(output.lower().split())
    if not expected_words:
        return 1.0
    overlap = expected_words & output_words
    return len(overlap) / len(expected_words)


def score_format_quality(output: str) -> float:
    """Score structural quality of output."""
    score = 0.5  # base
    if any(c in output for c in ["#", "**", "- ", "1. "]):
        score += 0.2  # has structure
    if len(output.split("\n")) > 3:
        score += 0.1  # multi-line
    if len(output) > 50:
        score += 0.1  # substantive
    if output.strip().endswith((".", "!", "?", "```")):
        score += 0.1  # proper ending
    return min(score, 1.0)


SCORERS = {
    "exact_match": score_exact_match,
    "contains": score_contains,
    "length_ratio": score_length_ratio,
    "keyword_coverage": score_keyword_coverage,
}


def evaluate_output(output: str, expected: str, scorers: list[str] | None = None) -> dict:
    """Run multiple scoring functions on an output."""
    if scorers is None:
        scorers = list(SCORERS.keys())
    scores = {}
    for name in scorers:
        if name in SCORERS:
            scores[name] = round(SCORERS[name](output, expected), 3)
    scores["format_quality"] = round(score_format_quality(output), 3)
    scores["average"] = round(sum(scores.values()) / len(scores), 3) if scores else 0
    return scores


def run_benchmark(cases: list[BenchmarkCase], model_outputs: dict[str, list[str]]) -> BenchmarkReport:
    """Run benchmark with pre-generated model outputs."""
    report = BenchmarkReport(models=list(model_outputs.keys()))
    model_scores = {m: [] for m in model_outputs}

    for i, case in enumerate(cases):
        for model, outputs in model_outputs.items():
            output = outputs[i] if i < len(outputs) else ""
            scores = evaluate_output(output, case.expected)
            result = ModelResult(model=model, prompt=case.prompt, output=output,
                                token_count=len(output.split()), scores=scores)
            report.results.append(result)
            model_scores[model].append(scores.get("average", 0))

    # Summary
    report.summary = {
        model: {
            "avg_score": round(sum(s) / len(s), 3) if s else 0,
            "cases_run": len(s),
        }
        for model, s in model_scores.items()
    }

    # Winner
    if report.summary:
        winner = max(report.summary.items(), key=lambda x: x[1].get("avg_score", 0))
        report.summary["winner"] = winner[0]

    return report


class BenchmarkStorage:
    def __init__(self, filepath: str | None = None):
        self.filepath = filepath or Config.STORAGE_FILE
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath) or ".", exist_ok=True)
            with open(self.filepath, "w") as f: json.dump([], f)

    def save(self, report: BenchmarkReport):
        data = self._load()
        data.append(report.to_dict())
        with open(self.filepath, "w") as f: json.dump(data, f, indent=2)

    def _load(self):
        try:
            with open(self.filepath) as f: return json.load(f)
        except: return []

    def get_all(self) -> list[dict]:
        return self._load()


def format_report_markdown(report: BenchmarkReport) -> str:
    """Format benchmark report as Markdown."""
    lines = [
        "# Benchmark Report",
        f"**Models:** {', '.join(report.models)}",
        f"**Cases:** {len(report.results) // max(len(report.models), 1)}",
        "",
        "## Results",
        "| Model | Avg Score | Cases |",
        "|-------|-----------|-------|",
    ]
    for model, data in report.summary.items():
        if model == "winner":
            continue
        score = data.get("avg_score", 0)
        cases = data.get("cases_run", 0)
        lines.append(f"| {model} | {score:.3f} | {cases} |")

    winner = report.summary.get("winner", "N/A")
    lines.extend(["", f"## 🏆 Winner: **{winner}**"])
    return "\n".join(lines)
