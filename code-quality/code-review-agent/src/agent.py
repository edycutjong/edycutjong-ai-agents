"""Code Review Agent — core Gemini logic."""
import json
import google.generativeai as genai
from config import Config

REVIEW_PROMPT = """\
You are a senior code reviewer. Analyze the following code and produce a JSON object with these fields:

- style_issues: list of objects with "line", "issue", "suggestion"
- bugs: list of objects with "line", "description", "severity" (critical/high/medium/low)
- security_issues: list of objects with "line", "vulnerability", "recommendation"
- performance_tips: list of strings
- complexity_rating: integer 1-10 (10 = most complex)
- overall_quality: integer 1-10 (10 = excellent)
- summary: a brief review summary

Code:
```
{code}
```

Respond ONLY with valid JSON.
"""


class CodeReviewAgent:
    """Review code using Gemini."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL)

    def review(self, code: str) -> dict:
        """Analyze code and return review results."""
        prompt = REVIEW_PROMPT.format(code=code)
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0].strip()
        return json.loads(text)
