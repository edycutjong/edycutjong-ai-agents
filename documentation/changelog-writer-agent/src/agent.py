"""Changelog Writer Agent — core Gemini logic."""
import json
import google.generativeai as genai
from config import Config

CHANGELOG_PROMPT = """\
You are a changelog writer. Given the following git commits, generate a professional Markdown changelog with:

1. A header with today's date
2. Sections: "### New Features", "### Bug Fixes", "### Improvements", "### Breaking Changes", "### Internal Changes"
3. Each entry as a bullet point, rewritten to be clear for end-users
4. Version bump suggestion (major/minor/patch) based on the changes

Commits:
{commits}

Respond with the FULL Markdown changelog text. Do not wrap in code fences.
"""


class ChangelogWriterAgent:
    """Generate changelogs using Gemini."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL)

    def generate(self, commits_text: str) -> str:
        """Generate a changelog from formatted commit text."""
        prompt = CHANGELOG_PROMPT.format(commits=commits_text)
        response = self.model.generate_content(prompt)
        return response.text.strip()
