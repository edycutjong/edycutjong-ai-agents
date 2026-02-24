"""Resume Tailor Agent — core Gemini logic."""
import json
import google.generativeai as genai
from config import Config

TAILOR_PROMPT = """\
You are a resume optimization specialist. Given a resume and a job description, produce a JSON object with:

- matched_keywords: list of keywords from the JD found in the resume
- missing_keywords: list of important JD keywords NOT in the resume
- skills_alignment: object with "matched" (list) and "gaps" (list)
- experience_suggestions: list of objects with "original", "improved" (rewritten bullet points)
- ats_score: integer 1-100 (100 = perfectly optimized)
- quality_score: integer 1-10
- summary: brief optimization summary

Resume:
{resume}

Job Description:
{job_description}

Respond ONLY with valid JSON.
"""


class ResumeTailorAgent:
    """Tailor resumes to job descriptions using Gemini."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL)

    def tailor(self, resume: str, job_description: str) -> dict:
        """Analyze resume against JD and return optimization results."""
        prompt = TAILOR_PROMPT.format(resume=resume, job_description=job_description)
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0].strip()
        return json.loads(text)
