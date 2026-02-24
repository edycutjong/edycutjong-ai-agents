"""Meeting Notes Summarizer — core Gemini logic."""
import json
import google.generativeai as genai
from config import Config

SUMMARY_PROMPT = """\
You are a meeting notes specialist. Analyze the following meeting transcript and produce a JSON object with:

- title: meeting title or topic
- date: date mentioned or "Unknown"
- attendees: list of names mentioned
- key_points: list of key discussion points
- action_items: list of objects with "task", "assignee", "deadline" (if mentioned)
- decisions: list of decisions made
- follow_ups: list of follow-up items
- metadata: object with "duration_mentioned", "meeting_type"
- summary: a concise executive summary (2-3 sentences)

Transcript:
{transcript}

Respond ONLY with valid JSON.
"""


class MeetingSummarizerAgent:
    """Summarize meeting transcripts using Gemini."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL)

    def summarize(self, transcript: str) -> dict:
        """Analyze a meeting transcript and return structured summary."""
        prompt = SUMMARY_PROMPT.format(transcript=transcript)
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0].strip()
        return json.loads(text)
