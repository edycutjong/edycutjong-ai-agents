"""Prompt optimization engine — analyze, score, and improve LLM prompts."""
from __future__ import annotations

import re
from dataclasses import dataclass, field


BEST_PRACTICES = {
    "specificity": {
        "description": "Be specific about the desired output format and content",
        "positive_indicators": [r"format as", r"output as", r"respond (?:with|in)", r"return (?:a|the)", r"provide (?:a|the)", r"give me", r"list \d+"],
        "negative_indicators": [r"^(?:tell|help|do|make)\s", r"^(?:can you|could you|please)\s*$"],
    },
    "role_setting": {
        "description": "Set a clear role or persona for the AI",
        "positive_indicators": [r"you are (?:a|an)", r"act as", r"role", r"expert", r"specialist", r"persona"],
        "negative_indicators": [],
    },
    "examples": {
        "description": "Include examples (few-shot prompting)",
        "positive_indicators": [r"example:", r"for example", r"e\.g\.", r"such as", r"like this:", r"input:.*output:"],
        "negative_indicators": [],
    },
    "constraints": {
        "description": "Define clear constraints and boundaries",
        "positive_indicators": [r"must not", r"do not", r"avoid", r"limit", r"only", r"maximum", r"minimum", r"between \d+ and \d+"],
        "negative_indicators": [],
    },
    "context": {
        "description": "Provide relevant context and background",
        "positive_indicators": [r"context:", r"background:", r"given that", r"assuming", r"based on", r"the (?:goal|objective|purpose) is"],
        "negative_indicators": [],
    },
    "output_structure": {
        "description": "Specify the desired output structure",
        "positive_indicators": [r"json", r"markdown", r"bullet", r"table", r"csv", r"numbered list", r"step.by.step", r"format:"],
        "negative_indicators": [],
    },
    "chain_of_thought": {
        "description": "Request reasoning or step-by-step thinking",
        "positive_indicators": [r"step.by.step", r"think.*through", r"reason.*about", r"explain.*reasoning", r"chain of thought", r"let'?s think"],
        "negative_indicators": [],
    },
}


@dataclass
class PromptScore:
    """Detailed scoring of a prompt's quality."""
    total_score: int = 0  # 0-100
    category_scores: dict = field(default_factory=dict)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    word_count: int = 0
    token_estimate: int = 0

    def to_dict(self) -> dict:
        return {
            "score": self.total_score, "word_count": self.word_count,
            "token_estimate": self.token_estimate,
            "category_scores": self.category_scores,
            "strengths": self.strengths, "weaknesses": self.weaknesses,
            "suggestions": self.suggestions,
        }


def analyze_prompt(prompt: str) -> PromptScore:
    """Score and analyze a prompt's effectiveness."""
    result = PromptScore()
    result.word_count = len(prompt.split())
    result.token_estimate = int(result.word_count * 1.3)

    lower = prompt.lower()
    total = 0
    count = 0

    for category, rules in BEST_PRACTICES.items():
        score = 0
        has_positive = any(re.search(p, lower) for p in rules["positive_indicators"])
        has_negative = any(re.search(p, lower) for p in rules.get("negative_indicators", []))

        if has_positive:
            score = 100
            result.strengths.append(f"✅ {rules['description']}")
        elif has_negative:
            score = 20
            result.weaknesses.append(f"❌ {rules['description']}")
            result.suggestions.append(f"💡 {rules['description']}")
        else:
            score = 50
            result.suggestions.append(f"💡 Consider: {rules['description']}")

        result.category_scores[category] = score
        total += score
        count += 1

    # Length bonus/penalty
    if result.word_count < 10:
        result.weaknesses.append("❌ Prompt is very short — add more detail")
        total -= 50
    elif result.word_count > 500:
        result.weaknesses.append("⚠️ Prompt is very long — consider condensing")

    result.total_score = max(0, min(100, total // count if count > 0 else 0))
    return result


def optimize_prompt(prompt: str) -> str:
    """Apply automatic optimizations to a prompt."""
    optimized = prompt.strip()

    # Add structure markers if missing
    if "step" not in optimized.lower() and len(optimized.split()) > 20:
        optimized = optimized + "\n\nPlease think step-by-step."

    # Add output format hint if missing
    if not re.search(r"format|output|respond|return", optimized, re.IGNORECASE):
        optimized = optimized + "\n\nProvide your response in a clear, structured format."

    return optimized


def compare_prompts(prompt_a: str, prompt_b: str) -> dict:
    """Compare two prompts and return which is better."""
    score_a = analyze_prompt(prompt_a)
    score_b = analyze_prompt(prompt_b)

    return {
        "prompt_a_score": score_a.total_score,
        "prompt_b_score": score_b.total_score,
        "winner": "A" if score_a.total_score > score_b.total_score else "B" if score_b.total_score > score_a.total_score else "Tie",
        "difference": abs(score_a.total_score - score_b.total_score),
    }


def format_analysis_markdown(result: PromptScore) -> str:
    """Format prompt analysis as Markdown."""
    bar = "█" * (result.total_score // 10) + "░" * (10 - result.total_score // 10)
    lines = [
        "# Prompt Analysis",
        "",
        f"**Score:** {result.total_score}/100 [{bar}]",
        f"**Words:** {result.word_count} | **Est. Tokens:** {result.token_estimate}",
        "",
    ]

    if result.category_scores:
        lines.append("## Category Scores")
        for cat, score in result.category_scores.items():
            emoji = "✅" if score >= 80 else "🟡" if score >= 50 else "❌"
            lines.append(f"- {emoji} **{cat}:** {score}/100")
        lines.append("")

    if result.strengths:
        lines.append("## Strengths")
        for s in result.strengths:
            lines.append(f"- {s}")
        lines.append("")

    if result.suggestions:
        lines.append("## Suggestions")
        for s in result.suggestions:
            lines.append(f"- {s}")

    return "\n".join(lines)
