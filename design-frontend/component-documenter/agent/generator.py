import os
import sys

# Ensure the parent directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from config import Config
from prompts.templates import DOC_PROMPT

class ComponentDocumenter:
    """
    Agent responsible for generating component documentation.
    """
    def __init__(self, api_key: str = None):
        """
        Initialize the documenter with an API key.
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API Key is required.")

        self.llm = ChatOpenAI(
            model=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            openai_api_key=self.api_key
        )

        # Create the chain
        self.chain = DOC_PROMPT | self.llm

    def generate_documentation(self, code: str, language: str) -> str:
        """
        Generates documentation for the given component code.
        """
        try:
            response = self.chain.invoke({
                "language": language,
                "code": code
            })
            return response.content
        except Exception as e:
            return f"Error generating documentation: {str(e)}"
