"""Email Draft Agent — core Gemini logic."""
import json
import google.generativeai as genai
from config import Config

DRAFT_PROMPT = """\
You are a professional email writing assistant. Given bullet points and parameters, compose a polished email draft.

Parameters:
- Tone: {tone}
- Length: {length}
- Thread context (if any): {context}

Bullet points to expand:
{bullet_points}

Produce a JSON object with:
- subject: a concise email subject line
- greeting: appropriate greeting
- body: the full email body (well-structured paragraphs)
- closing: professional closing line
- full_draft: the complete email as a single string (greeting + body + closing)

Respond ONLY with valid JSON.
"""

TONES = ["formal", "casual", "friendly", "urgent", "apologetic"]
LENGTHS = ["short", "medium", "long"]


class EmailDraftAgent:
    """Draft professional emails using Gemini."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL)

    def draft(self, bullet_points: str, tone: str = "formal",
              length: str = "medium", context: str = "") -> dict:
        """Generate an email draft from bullet points."""
        prompt = DRAFT_PROMPT.format(
            tone=tone,
            length=length,
            context=context or "None",
            bullet_points=bullet_points,
        )
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0].strip()
        return json.loads(text)
