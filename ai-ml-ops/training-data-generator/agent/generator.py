"""Training data generator — create synthetic training datasets for LLMs."""
from __future__ import annotations

import json, random, re
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TrainingExample:
    """A single training example."""
    instruction: str
    input: str = ""
    output: str = ""
    category: str = ""
    quality: float = 1.0  # 0-1

    def to_alpaca(self) -> dict:
        return {"instruction": self.instruction, "input": self.input, "output": self.output}

    def to_chat(self) -> dict:
        msgs = [{"role": "system", "content": "You are a helpful assistant."}]
        prompt = self.instruction
        if self.input:
            prompt += f"\n\n{self.input}"
        msgs.append({"role": "user", "content": prompt})
        msgs.append({"role": "assistant", "content": self.output})
        return {"messages": msgs}

    def to_completion(self) -> dict:
        prompt = self.instruction
        if self.input:
            prompt += f"\n{self.input}"
        return {"prompt": prompt, "completion": self.output}


# --- Template Library ---

TEMPLATES = {
    "qa": [
        {"instruction": "Answer the following question.", "input": "What is {topic}?", "output": "{topic} is {definition}."},
        {"instruction": "Explain {topic} in simple terms.", "output": "{topic} can be understood as {definition}."},
        {"instruction": "Define {topic}.", "output": "{definition}"},
    ],
    "classification": [
        {"instruction": "Classify the following text as positive, negative, or neutral.", "input": "{text}", "output": "{label}"},
        {"instruction": "What is the sentiment of this review?", "input": "{text}", "output": "The sentiment is {label}."},
    ],
    "summarization": [
        {"instruction": "Summarize the following text.", "input": "{text}", "output": "{summary}"},
        {"instruction": "Provide a brief summary.", "input": "{text}", "output": "{summary}"},
    ],
    "translation": [
        {"instruction": "Translate the following to {target_lang}.", "input": "{text}", "output": "{translation}"},
    ],
    "code": [
        {"instruction": "Write a {language} function that {task}.", "output": "```{language}\n{code}\n```"},
        {"instruction": "Fix the bug in this code.", "input": "```{language}\n{code}\n```", "output": "```{language}\n{fixed_code}\n```"},
    ],
    "extraction": [
        {"instruction": "Extract key information from the text.", "input": "{text}", "output": "{extracted}"},
    ],
}


def generate_from_template(category: str, variables: dict, count: int = 1) -> list[TrainingExample]:
    """Generate training examples from templates."""
    templates = TEMPLATES.get(category, [])
    if not templates:
        return []

    examples = []
    for _ in range(count):
        template = random.choice(templates)
        instruction = template["instruction"]
        inp = template.get("input", "")
        output = template.get("output", "")

        for key, value in variables.items():
            instruction = instruction.replace(f"{{{key}}}", str(value))
            inp = inp.replace(f"{{{key}}}", str(value))
            output = output.replace(f"{{{key}}}", str(value))

        examples.append(TrainingExample(
            instruction=instruction, input=inp, output=output, category=category,
        ))
    return examples


def generate_variations(example: TrainingExample, count: int = 3) -> list[TrainingExample]:
    """Generate variations of an existing example."""
    variations = []
    prefixes = ["Please ", "Could you ", "I need you to ", "Help me ", ""]
    suffixes = ["", " Be concise.", " Provide a detailed answer.", " Think step by step."]

    for i in range(count):
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        varied = TrainingExample(
            instruction=f"{prefix}{example.instruction.lower()}{suffix}".strip().capitalize(),
            input=example.input, output=example.output, category=example.category,
        )
        variations.append(varied)
    return variations


def validate_dataset(examples: list[TrainingExample]) -> dict:
    """Validate a training dataset for quality."""
    issues = []
    stats = {"total": len(examples), "categories": {}, "avg_instruction_length": 0, "avg_output_length": 0}

    total_inst_len = 0
    total_out_len = 0
    seen_instructions = set()

    for i, ex in enumerate(examples):
        if not ex.instruction.strip():
            issues.append(f"Example {i}: empty instruction")
        if not ex.output.strip():
            issues.append(f"Example {i}: empty output")
        if len(ex.instruction) < 10:
            issues.append(f"Example {i}: instruction too short ({len(ex.instruction)} chars)")
        if ex.instruction in seen_instructions:
            issues.append(f"Example {i}: duplicate instruction")
        seen_instructions.add(ex.instruction)

        stats["categories"][ex.category] = stats["categories"].get(ex.category, 0) + 1
        total_inst_len += len(ex.instruction)
        total_out_len += len(ex.output)

    stats["avg_instruction_length"] = round(total_inst_len / max(len(examples), 1))
    stats["avg_output_length"] = round(total_out_len / max(len(examples), 1))
    stats["issues"] = issues
    stats["quality_score"] = max(0, 100 - len(issues) * 10)
    return stats


def export_dataset(examples: list[TrainingExample], fmt: str = "alpaca") -> str:
    """Export dataset in various formats."""
    if fmt == "alpaca":
        return json.dumps([e.to_alpaca() for e in examples], indent=2)
    elif fmt == "chat":
        return json.dumps([e.to_chat() for e in examples], indent=2)
    elif fmt == "completion":
        return "\n".join(json.dumps(e.to_completion()) for e in examples)
    elif fmt == "jsonl":
        return "\n".join(json.dumps(e.to_alpaca()) for e in examples)
    return json.dumps([e.to_alpaca() for e in examples], indent=2)


def format_stats_markdown(stats: dict) -> str:
    """Format validation stats as Markdown."""
    lines = [
        "# Training Data Report",
        f"**Total Examples:** {stats['total']}",
        f"**Quality Score:** {stats.get('quality_score', 0)}/100",
        f"**Avg Instruction Length:** {stats['avg_instruction_length']} chars",
        f"**Avg Output Length:** {stats['avg_output_length']} chars",
        "",
    ]
    if stats.get("categories"):
        lines.append("## Categories")
        for cat, count in stats["categories"].items():
            lines.append(f"- **{cat}:** {count}")
    if stats.get("issues"):
        lines.extend(["", "## ⚠️ Issues"])
        for issue in stats["issues"][:10]:
            lines.append(f"- {issue}")
    return "\n".join(lines)
