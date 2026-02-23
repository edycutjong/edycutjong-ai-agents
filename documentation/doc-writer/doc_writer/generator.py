from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .config import config
from .utils import logger

class DocGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config.MODEL_NAME,
            temperature=0.2,
            api_key=config.OPENAI_API_KEY
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert Python documentation writer. Generate a Google-style docstring for the provided code snippet. Output ONLY the docstring content, without the triple quotes."),
            ("user", "{code_snippet}")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()

    def generate_docstring(self, code_snippet: str) -> str:
        try:
            docstring = self.chain.invoke({"code_snippet": code_snippet})
            docstring = docstring.strip()

            # Strip triple quotes if present in the LLM output
            if docstring.startswith('"""') and docstring.endswith('"""'):
                docstring = docstring[3:-3].strip()
            elif docstring.startswith("'''") and docstring.endswith("'''"):
                docstring = docstring[3:-3].strip()

            return docstring
        except Exception as e:
            # Fallback or re-raise depending on requirements.
            # For now, let's log and re-raise or return empty.
            logger.error(f"Error generating docstring: {e}")
            return ""
