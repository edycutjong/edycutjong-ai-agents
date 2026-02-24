"""Dependency Update Agent — core Gemini logic."""
import json
import google.generativeai as genai
from config import Config

DEPENDENCY_PROMPT = """\
You are a dependency management specialist. Analyze the following dependency list and produce a JSON object with these fields:

- updates: list of objects with "package", "current_version", "latest_version", "update_type" (major/minor/patch), "risk_level" (high/medium/low), "breaking_changes" (boolean), "changelog_url" (string or null)
- batch_plan: list of strings describing the recommended update order
- total_outdated: integer count of outdated deps
- summary: a brief summary of the dependency health

Dependency file content:
```
{deps_content}
```

Respond ONLY with valid JSON.
"""


class DependencyUpdateAgent:
    """Analyze dependency updates using Gemini."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL)

    def analyze(self, deps_content: str) -> dict:
        """Analyze dependencies and return update recommendations."""
        prompt = DEPENDENCY_PROMPT.format(deps_content=deps_content)
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0].strip()
        return json.loads(text)
