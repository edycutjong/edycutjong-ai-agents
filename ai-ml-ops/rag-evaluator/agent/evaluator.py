import os
import sys
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import Config
from prompts.evaluation_prompts import (
    FAITHFULNESS_PROMPT,
    ANSWER_RELEVANCE_PROMPT,
    CONTEXT_PRECISION_PROMPT
)

class RAGEvaluator:
    def __init__(self, openai_api_key: str = None, model_name: str = "gpt-3.5-turbo"):
        self.api_key = openai_api_key or Config.OPENAI_API_KEY
        self.llm = ChatOpenAI(
            model=model_name,
            openai_api_key=self.api_key,
            temperature=0
        )

    def _get_score(self, prompt, **kwargs) -> float:
        """Helper to invoke LLM and parse score."""
        chain = prompt | self.llm | StrOutputParser()
        try:
            result = chain.invoke(kwargs)
            # improved parsing to handle potential text around the number
            import re
            match = re.search(r"(\d+(\.\d+)?)", result)
            if match:
                return float(match.group(1))
            return 0.0
        except Exception as e:
            print(f"Error calculating score: {e}")
            return 0.0

    def evaluate_faithfulness(self, answer: str, context: str) -> float:
        return self._get_score(FAITHFULNESS_PROMPT, answer=answer, context=context)

    def evaluate_answer_relevance(self, question: str, answer: str) -> float:
        return self._get_score(ANSWER_RELEVANCE_PROMPT, question=question, answer=answer)

    def evaluate_context_precision(self, question: str, context: str) -> float:
        return self._get_score(CONTEXT_PRECISION_PROMPT, question=question, context=context)

    def evaluate(self, question: str, answer: str, context: str) -> Dict[str, float]:
        """Runs all evaluations and returns a dictionary of scores."""
        return {
            "faithfulness": self.evaluate_faithfulness(answer, context),
            "answer_relevance": self.evaluate_answer_relevance(question, answer),
            "context_precision": self.evaluate_context_precision(question, context)
        }
