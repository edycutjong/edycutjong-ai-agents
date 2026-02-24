"""I18N Translator Agent — core Gemini logic."""
import json
import google.generativeai as genai
from config import Config

TRANSLATE_PROMPT = """\
You are an expert i18n translator. Translate the following JSON i18n file to {target_language}.

Rules:
1. Preserve ALL JSON keys exactly as-is (do not translate keys)
2. Preserve ALL placeholders like {{{{name}}}}, {{{{count}}}}, %s, %d, {{0}}, etc.
3. Maintain the same JSON structure and nesting
4. Use natural, contextually appropriate translations (not word-for-word)
5. Preserve any HTML tags in values

Source JSON ({source_language}):
```json
{source_json}
```

Respond ONLY with the translated JSON object. No markdown fences, no explanations.
"""

QUALITY_PROMPT = """\
Review this i18n translation for quality. Source ({source_language}) and target ({target_language}):

Source:
{source_json}

Translation:
{translated_json}

Produce a JSON object with:
- quality_score: integer 1-10
- issues: list of objects with "key", "issue", "suggestion"
- placeholder_errors: list of keys where placeholders were modified
- summary: brief quality summary

Respond ONLY with valid JSON.
"""


class I18nTranslatorAgent:
    """Translate i18n JSON files using Gemini."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL)

    def translate(self, source_json: str, target_language: str, source_language: str = "English") -> dict:
        """Translate an i18n JSON file to a target language."""
        prompt = TRANSLATE_PROMPT.format(
            target_language=target_language,
            source_language=source_language,
            source_json=source_json,
        )
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0].strip()
        return json.loads(text)

    def review_quality(self, source_json: str, translated_json: str, source_language: str = "English", target_language: str = "Unknown") -> dict:
        """Review translation quality."""
        prompt = QUALITY_PROMPT.format(
            source_language=source_language,
            target_language=target_language,
            source_json=source_json,
            translated_json=translated_json,
        )
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0].strip()
        return json.loads(text)
