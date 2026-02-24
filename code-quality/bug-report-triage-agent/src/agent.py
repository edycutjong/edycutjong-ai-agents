"""Bug Report Triage Agent — core Gemini logic."""
import json
import google.generativeai as genai
from config import Config

TRIAGE_PROMPT = """\
You are a bug report triage specialist. Analyze the following bug report and produce a JSON object with these fields:

- severity: one of "critical", "high", "medium", "low"
- component: the likely affected component or module
- is_duplicate: boolean, true if this seems like a duplicate of a common issue
- priority_score: integer 1-10 (10 = most urgent)
- suggested_assignee: team or role best suited to handle this
- labels: list of relevant labels/tags
- summary: a one-line triage summary

Bug Report:
{bug_report}

Respond ONLY with valid JSON.
"""


class BugTriageAgent:
    """Triage bug reports using Gemini."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL)

    def triage(self, bug_report: str) -> dict:
        """Analyze a bug report and return triage results."""
        prompt = TRIAGE_PROMPT.format(bug_report=bug_report)
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        # Strip markdown fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0].strip()
        return json.loads(text)
