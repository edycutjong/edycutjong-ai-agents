"""README generator — generate project README files from metadata."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ReadmeResult:
    content: str = ""; sections: list[str] = field(default_factory=list); word_count: int = 0
    def to_dict(self) -> dict: return {"sections": len(self.sections), "words": self.word_count}

def generate(name: str, description: str = "", features: list[str] = None, install: str = "", usage: str = "", license_type: str = "MIT", author: str = "") -> ReadmeResult:
    r = ReadmeResult()
    lines = [f"# {name}", ""]
    if description: lines.extend([description, ""]); r.sections.append("description")
    if features:
        lines.extend(["## Features", ""]); r.sections.append("features")
        for f in features: lines.append(f"- {f}")
        lines.append("")
    if install:
        lines.extend(["## Installation", "", "```bash", install, "```", ""]); r.sections.append("installation")
    if usage:
        lines.extend(["## Usage", "", "```", usage, "```", ""]); r.sections.append("usage")
    lines.extend(["## License", "", f"This project is licensed under the {license_type} License.", ""])
    r.sections.append("license")
    if author: lines.extend([f"---", f"Built by **{author}**", ""])
    r.content = "\n".join(lines); r.word_count = len(r.content.split())
    return r

def add_badges(content: str, badges: list[dict]) -> str:
    badge_lines = []
    for b in badges:
        badge_lines.append(f"[![{b.get('label', '')}]({b.get('url', '')})]({b.get('link', '#')})")
    return "\n".join(badge_lines) + "\n\n" + content if badge_lines else content

def add_toc(content: str) -> str:
    import re
    headings = re.findall(r'^(#{2,3})\s+(.+)$', content, re.MULTILINE)
    if not headings: return content
    toc = ["## Table of Contents", ""]
    for h, title in headings:
        indent = "  " * (len(h) - 2)
        anchor = title.lower().replace(" ", "-")
        toc.append(f"{indent}- [{title}](#{anchor})")
    toc.append("")
    first_section = content.find("\n## ")
    if first_section > 0:
        return content[:first_section] + "\n" + "\n".join(toc) + content[first_section:]
    return "\n".join(toc) + "\n" + content

def format_result_markdown(r: ReadmeResult) -> str:
    return f"## README Generator 📖\n**Sections:** {len(r.sections)} | **Words:** {r.word_count}"
