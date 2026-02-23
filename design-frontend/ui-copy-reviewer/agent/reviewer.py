import os
import sys

# Ensure parent directory is in path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_community.llms import FakeListLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import config
from prompts.system_prompts import (
    INCLUSIVE_LANGUAGE_PROMPT,
    CONSISTENCY_PROMPT,
    JARGON_PROMPT,
    LOCALIZABILITY_PROMPT,
    CLARITY_PROMPT,
    VOICE_TONE_PROMPT
)

class ReviewerAgent:
    def __init__(self):
        self.llm = self._get_llm()
        self.checks = {
            "Inclusive Language": INCLUSIVE_LANGUAGE_PROMPT,
            "Consistency": CONSISTENCY_PROMPT,
            "Jargon": JARGON_PROMPT,
            "Localizability": LOCALIZABILITY_PROMPT,
            "Clarity": CLARITY_PROMPT,
            "Voice & Tone": VOICE_TONE_PROMPT
        }

    def _get_llm(self):
        if config.USE_MOCK_LLM or not config.OPENAI_API_KEY:
            # Return a fake LLM for testing/demo without keys
            responses = [
                "OK",
                "Suggestion: Use 'Sign In' instead of 'Log On'.",
                "Flag: 'Pwned' is jargon.",
                "OK",
                "Suggestion: Simplify 'utilize' to 'use'.",
                "Tone: Should be more friendly."
            ]
            return FakeListLLM(responses=responses * 10) # Repeat to avoid running out
        else:
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0,
                api_key=config.OPENAI_API_KEY
            )

    def review_text(self, text, context=None):
        """
        Reviews a single piece of text against all configured checks.
        Returns a dictionary of issues found.
        """
        results = {}

        for check_name, prompt_template in self.checks.items():
            prompt = PromptTemplate.from_template(prompt_template)
            chain = prompt | self.llm | StrOutputParser()

            try:
                response = chain.invoke({"text": text})
                if response.strip().upper() != "OK" and "OK" not in response.strip().upper().split():
                     # Simple heuristic: if LLM says OK, no issue.
                     # If it provides text, there's likely an issue or suggestion.
                     # However, sometimes it might say "The text is OK."
                     # So we should be careful. The prompt asks to return "OK".
                     # Let's trust the prompt instruction for now.
                     if "OK" not in response[:5].upper():
                        results[check_name] = response.strip()
            except Exception as e:
                results[check_name] = f"Error during review: {str(e)}"

        return results

    def review_items(self, items):
        """
        Reviews a list of extracted items.
        Returns the list with an added 'issues' key for each item if issues are found.
        """
        reviewed_items = []
        for item in items:
            text = item.get('text', '')
            if not text:
                continue

            # Skip very short strings or numbers
            if len(text) < 3 or text.isdigit():
                continue

            issues = self.review_text(text, context=item.get('context'))
            if issues:
                item['issues'] = issues
                reviewed_items.append(item)

        return reviewed_items
