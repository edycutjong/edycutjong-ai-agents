import json
import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from prompts.system_prompts import (
    SUMMARY_PROMPT,
    ACTION_EXTRACTION_PROMPT,
    EMAIL_DRAFT_PROMPT,
    SPEAKER_DIARIZATION_PROMPT,
)
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MeetingProcessor:
    def __init__(self, api_key=None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        if self.api_key:
            self.llm = ChatOpenAI(
                model=Config.DEFAULT_MODEL,
                temperature=0,
                openai_api_key=self.api_key
            )
        else:
            self.llm = None
            logger.warning("OpenAI API Key not found. Processor will fail on execution.")

    def process_transcript(self, transcript):
        if not self.llm:
            return {
                "error": "OpenAI API Key is missing. Please configure it in .env or the sidebar."
            }

        try:
            logger.info("Generating summary...")
            summary = self._generate_summary(transcript)

            logger.info("Extracting action items...")
            action_items = self._extract_action_items(transcript)

            logger.info("Identifying speakers...")
            speakers = self._extract_speakers(transcript)

            logger.info("Drafting email...")
            email_draft = self._draft_email(summary, action_items)

            return {
                "summary": summary,
                "action_items": action_items,
                "speakers": speakers,
                "email_draft": email_draft,
            }
        except Exception as e:
            logger.error(f"Error processing transcript: {e}")
            return {
                "error": str(e)
            }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def _generate_summary(self, transcript):
        prompt = ChatPromptTemplate.from_messages([
            ("system", SUMMARY_PROMPT),
            ("user", "{transcript}")
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"transcript": transcript})

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def _extract_action_items(self, transcript):
        prompt = ChatPromptTemplate.from_messages([
            ("system", ACTION_EXTRACTION_PROMPT),
            ("user", "{transcript}")
        ])
        chain = prompt | self.llm | StrOutputParser()
        result_str = chain.invoke({"transcript": transcript})
        return self._parse_json_response(result_str)

    @staticmethod
    def _parse_json_response(result_str):
        """Parse JSON from LLM response, stripping markdown code blocks."""
        if "```json" in result_str:
            result_str = result_str.split("```json")[1].split("```")[0].strip()
        elif "```" in result_str:
            result_str = result_str.split("```")[1].split("```")[0].strip()

        try:
            return json.loads(result_str)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON: {result_str}")
            return []

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def _extract_speakers(self, transcript):
        """Identify unique speakers and their contributions."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", SPEAKER_DIARIZATION_PROMPT),
            ("user", "{transcript}")
        ])
        chain = prompt | self.llm | StrOutputParser()
        result_str = chain.invoke({"transcript": transcript})
        return self._parse_json_response(result_str)

    def _draft_email(self, summary, action_items):
        action_items_str = json.dumps(action_items, indent=2)
        prompt = ChatPromptTemplate.from_messages([
            ("system", EMAIL_DRAFT_PROMPT),
            ("user", "Please draft the email.")
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"summary": summary, "action_items": action_items_str})
