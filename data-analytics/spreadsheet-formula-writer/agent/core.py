import logging
from typing import Any, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableSequence

from agent.models import FormulaResponse
from prompts.templates import get_formula_prompt
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class FormulaWriterAgent:
    def __init__(
        self,
        model_name: str = "gpt-4o",
        temperature: float = 0.0,
        api_key: Optional[str] = None
    ):
        self.api_key = api_key or OPENAI_API_KEY

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment or config.py")

        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=self.api_key
        )
        self.parser = PydanticOutputParser(pydantic_object=FormulaResponse)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    def _invoke_chain(self, chain, query: str, target_application: str) -> FormulaResponse:
        """Helper method to invoke chain with retry logic."""
        return chain.invoke({
            "query": query,
            "target_application": target_application
        })

    def generate_formula(self, query: str, target_application: str = "Excel") -> FormulaResponse:
        """
        Generates a spreadsheet formula based on the user's query.

        Args:
            query: The natural language query describing the desired formula.
            target_application: The target application (e.g., "Excel", "Google Sheets").

        Returns:
            FormulaResponse: The structured response containing the formula and explanation.
        """
        logger.info(f"Generating formula for query: '{query}' (Target: {target_application})")

        prompt = get_formula_prompt()

        # Create the chain
        # ChatOpenAI.with_structured_output is preferred for reliability with OpenAI models.
        structured_llm = self.llm.with_structured_output(FormulaResponse)

        chain = prompt | structured_llm

        try:
            result = self._invoke_chain(chain, query, target_application)
            logger.info("Formula generated successfully.")
            return result
        except Exception as e:
            logger.error(f"Failed to generate formula: {str(e)}")
            raise RuntimeError(f"Failed to generate formula: {str(e)}")
