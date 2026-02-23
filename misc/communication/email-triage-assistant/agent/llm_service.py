import json
import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from .models import Email, TriageResult, DraftReply
from config import Config
from prompts.prompts import TRIAGE_PROMPT_TEMPLATE, DRAFT_REPLY_PROMPT_TEMPLATE, BRIEFING_PROMPT_TEMPLATE

class LLMService:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        if self.api_key:
            self.llm = ChatOpenAI(api_key=self.api_key, model="gpt-4o-mini", temperature=0)
        else:
            print("Warning: No OpenAI API Key found. Using Mock LLM.")
            self.llm = None

    def analyze_email(self, email: Email) -> TriageResult:
        if not self.llm:
            return self._mock_analyze_email(email)

        parser = JsonOutputParser(pydantic_object=TriageResult)
        prompt = PromptTemplate(
            template=TRIAGE_PROMPT_TEMPLATE,
            input_variables=["subject", "sender", "body"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        chain = prompt | self.llm | parser

        try:
            result = chain.invoke({
                "subject": email.subject,
                "sender": email.sender,
                "body": email.body
            })
            return TriageResult(**result)
        except Exception as e:
            print(f"Error analyzing email: {e}")
            return self._mock_analyze_email(email)

    def draft_reply(self, email: Email, instructions: str = "", tone: str = "professional") -> str:
        if not self.llm:
            return self._mock_draft_reply(email, instructions, tone)

        prompt = PromptTemplate(
            template=DRAFT_REPLY_PROMPT_TEMPLATE,
            input_variables=["subject", "sender", "body", "instructions", "tone"]
        )

        chain = prompt | self.llm | StrOutputParser()

        try:
            return chain.invoke({
                "subject": email.subject,
                "sender": email.sender,
                "body": email.body,
                "instructions": instructions,
                "tone": tone
            })
        except Exception as e:
            print(f"Error drafting reply: {e}")
            return self._mock_draft_reply(email, instructions, tone)

    def generate_briefing(self, emails: List[Email]) -> str:
        if not self.llm:
            return "This is a mock daily briefing. Please provide an OpenAI API Key to generate a real briefing based on your emails."

        if not emails:
            return "No high-priority emails to brief."

        prompt = PromptTemplate(
            template=BRIEFING_PROMPT_TEMPLATE,
            input_variables=["emails_text"]
        )

        emails_text = "\n\n".join([f"Subject: {e.subject}\nFrom: {e.sender}\nBody: {e.body[:200]}..." for e in emails])

        chain = prompt | self.llm | StrOutputParser()

        try:
            return chain.invoke({"emails_text": emails_text})
        except Exception as e:
            print(f"Error generating briefing: {e}")
            return "Error generating briefing."

    def _mock_analyze_email(self, email: Email) -> TriageResult:
        # Simple heuristic fallback
        category = "Other"
        urgency = 1
        summary = "Mock summary of the email."

        lower_sub = email.subject.lower()
        if "urgent" in lower_sub or "deadline" in lower_sub:
            category = "Urgent"
            urgency = 9
            summary = "This email seems urgent due to keywords in the subject."
        elif "newsletter" in lower_sub:
            category = "Newsletter"
            urgency = 2
        elif "invoice" in lower_sub:
            category = "Work"
            urgency = 7
            summary = "This appears to be a bill or invoice."

        return TriageResult(
            category=category,
            urgency_score=urgency,
            summary=summary,
            action_items=["Review email", "Reply if necessary"],
            suggested_actions=["Archive", "Reply"]
        )

    def _mock_draft_reply(self, email: Email, instructions: str, tone: str) -> str:
        return f"Dear {email.sender},\n\nThis is a mock reply generated because no API key was provided.\n\nRegarding: {email.subject}\n\nBest,\n[Your Name]"
