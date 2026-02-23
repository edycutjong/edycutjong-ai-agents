import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from prompts.system_prompts import ANALYZE_LOGS_PROMPT

class LogAnalyzer:
    def __init__(self, api_key: str = None, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(
            model=model_name,
            api_key=api_key or "sk-dummy",  # Fallback for dev/mock
            temperature=0
        )
        self.parser = JsonOutputParser()
        self.prompt = PromptTemplate(
            template=ANALYZE_LOGS_PROMPT,
            input_variables=["logs"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        self.chain = self.prompt | self.llm | self.parser

    def analyze_logs(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyzes a batch of logs using the LLM."""
        log_str = json.dumps(logs, indent=2)

        try:
            logger.info("Analyzing logs with LLM...")
            result = self.chain.invoke({"logs": log_str})
            logger.info("Analysis complete.")
            return result
        except Exception as e:
            logger.error(f"Error during log analysis: {e}")
            # Return a fallback/mock response if LLM fails (e.g., no key)
            return {
                "anomalies": ["LLM Analysis Failed"],
                "root_cause": "Could not connect to LLM API.",
                "remediation": "Check API key configuration.",
                "severity": "UNKNOWN",
                "summary": str(e)
            }
