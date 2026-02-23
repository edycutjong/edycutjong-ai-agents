"""Gitignore generator — generate .gitignore files for various tech stacks."""
from __future__ import annotations
from dataclasses import dataclass, field

TEMPLATES = {
    "python": ["__pycache__/", "*.py[cod]", "*$py.class", "*.so", ".Python", "build/", "dist/", "*.egg-info/", ".eggs/", "*.egg", ".venv/", "venv/", ".env", ".pytest_cache/", ".mypy_cache/", "htmlcov/", ".tox/"],
    "node": ["node_modules/", "npm-debug.log*", "yarn-debug.log*", "yarn-error.log*", ".pnpm-debug.log*", "dist/", "build/", ".env", ".env.local", ".next/", ".nuxt/", "coverage/", ".cache/"],
    "java": ["*.class", "*.jar", "*.war", "*.ear", "target/", ".gradle/", "build/", ".idea/", "*.iml", "out/", "bin/"],
    "go": ["*.exe", "*.dll", "*.so", "*.dylib", "*.test", "*.out", "vendor/", "bin/", ".env"],
    "rust": ["target/", "Cargo.lock", "**/*.rs.bk"],
    "general": [".DS_Store", "Thumbs.db", "*.log", ".env", ".env.local", "*.swp", "*.swo", "*~", ".idea/", ".vscode/", "*.bak", "*.tmp"],
}

@dataclass
class GitignoreResult:
    content: str = ""; languages: list[str] = field(default_factory=list)
    pattern_count: int = 0; custom_patterns: list[str] = field(default_factory=list)
    def to_dict(self) -> dict: return {"languages": self.languages, "patterns": self.pattern_count}

def generate(languages: list[str], custom: list[str] = None) -> GitignoreResult:
    r = GitignoreResult(languages=languages, custom_patterns=custom or [])
    lines = ["# Generated .gitignore", ""]
    lines.extend(["# General", ""] + TEMPLATES.get("general", []) + [""])
    for lang in languages:
        patterns = TEMPLATES.get(lang.lower(), [])
        if patterns:
            lines.extend([f"# {lang.capitalize()}", ""] + patterns + [""])
    if custom:
        lines.extend(["# Custom", ""] + custom + [""])
    r.content = "\n".join(lines)
    r.pattern_count = sum(1 for l in r.content.splitlines() if l.strip() and not l.startswith("#"))
    return r

def get_languages() -> list[str]:
    return [k for k in TEMPLATES if k != "general"]

def get_template(lang: str) -> list[str]:
    return TEMPLATES.get(lang.lower(), [])

def merge_gitignores(existing: str, new_patterns: list[str]) -> str:
    existing_lines = set(existing.splitlines())
    additions = [p for p in new_patterns if p not in existing_lines]
    if additions:
        return existing.rstrip() + "\n\n# Added\n" + "\n".join(additions) + "\n"
    return existing

def format_result_markdown(r: GitignoreResult) -> str:
    return f"## Gitignore Generator 📄\n**Languages:** {', '.join(r.languages)} | **Patterns:** {r.pattern_count}\n```gitignore\n{r.content[:300]}\n```"
