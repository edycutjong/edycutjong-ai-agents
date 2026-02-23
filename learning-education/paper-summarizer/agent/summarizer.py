from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from prompts.templates import (
    ABSTRACT_METHODOLOGY_PROMPT,
    PLAIN_LANGUAGE_SUMMARY_PROMPT,
    KEY_FINDINGS_PROMPT,
    CITATIONS_PROMPT,
)
import config

class PaperSummarizer:
    def __init__(self, model_name=config.MODEL_NAME, temperature=config.TEMPERATURE):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=config.OPENAI_API_KEY
        )

    def extract_abstract_methodology(self, text: str) -> str:
        chain = ABSTRACT_METHODOLOGY_PROMPT | self.llm | StrOutputParser()
        return chain.invoke({"text": text})

    def generate_plain_language_summary(self, text: str) -> str:
        chain = PLAIN_LANGUAGE_SUMMARY_PROMPT | self.llm | StrOutputParser()
        return chain.invoke({"text": text})

    def extract_key_findings(self, text: str) -> str:
        chain = KEY_FINDINGS_PROMPT | self.llm | StrOutputParser()
        return chain.invoke({"text": text})

    def extract_citations(self, text: str) -> str:
        chain = CITATIONS_PROMPT | self.llm | StrOutputParser()
        return chain.invoke({"text": text})

    def summarize_all(self, text: str) -> dict:
        """
        Runs all summarization tasks and returns a dictionary.
        """
        return {
            "abstract_methodology": self.extract_abstract_methodology(text),
            "plain_language_summary": self.generate_plain_language_summary(text),
            "key_findings": self.extract_key_findings(text),
            "citations": self.extract_citations(text),
        }
