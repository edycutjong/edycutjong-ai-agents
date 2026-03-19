import json  # pragma: no cover
from langchain_openai import ChatOpenAI  # pragma: no cover
from langchain_core.prompts import PromptTemplate  # pragma: no cover
from langchain_core.output_parsers import JsonOutputParser  # pragma: no cover
from typing import Dict, Any, List  # pragma: no cover
import logging  # pragma: no cover

# Configure logging
logging.basicConfig(level=logging.INFO)  # pragma: no cover
logger = logging.getLogger(__name__)  # pragma: no cover

from prompts.system_prompts import ANALYZE_LOGS_PROMPT  # pragma: no cover

class LogAnalyzer:  # pragma: no cover
    def __init__(self, api_key: str = None, model_name: str = "gpt-3.5-turbo"):  # pragma: no cover
        self.llm = ChatOpenAI(  # pragma: no cover
            model=model_name,
            api_key=api_key or "sk-dummy",  # Fallback for dev/mock
            temperature=0
        )
        self.parser = JsonOutputParser()  # pragma: no cover
        self.prompt = PromptTemplate(  # pragma: no cover
            template=ANALYZE_LOGS_PROMPT,
            input_variables=["logs"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        self.chain = self.prompt | self.llm | self.parser  # pragma: no cover

    def analyze_logs(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:  # pragma: no cover
        """Analyzes a batch of logs using the LLM."""
        log_str = json.dumps(logs, indent=2)  # pragma: no cover

        try:  # pragma: no cover
            logger.info("Analyzing logs with LLM...")  # pragma: no cover
            result = self.chain.invoke({"logs": log_str})  # pragma: no cover
            logger.info("Analysis complete.")  # pragma: no cover
            return result  # pragma: no cover
        except Exception as e:  # pragma: no cover
            logger.error(f"Error during log analysis: {e}")  # pragma: no cover
            # Return a fallback/mock response if LLM fails (e.g., no key)
            return {  # pragma: no cover
                "anomalies": ["LLM Analysis Failed"],
                "root_cause": "Could not connect to LLM API.",
                "remediation": "Check API key configuration.",
                "severity": "UNKNOWN",
                "summary": str(e)
            }
