import json
import yaml
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Use try-except block to handle both direct execution and package imports
try:
    from prompts.prompts import analysis_prompt
    from config import Config
except ImportError:  # pragma: no cover
    # Fallback for when running tests or from a different context where the path is different
    import sys  # pragma: no cover
    import os  # pragma: no cover
    # Add the project root to sys.path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # pragma: no cover
    if project_root not in sys.path:  # pragma: no cover
        sys.path.insert(0, project_root)  # pragma: no cover
    from prompts.prompts import analysis_prompt  # pragma: no cover
    from config import Config  # pragma: no cover

class CIAnalyzer:
    def __init__(self, llm):
        self.llm = llm
        if self.llm:
            self.analysis_chain = analysis_prompt | self.llm | JsonOutputParser()
        else:
            self.analysis_chain = None

    def analyze(self, config_content: str) -> dict:
        """
        Analyzes the CI/CD configuration file.
        """
        if not self.analysis_chain:
             return {"error": "LLM not initialized. Missing API Key."}

        try:
            # Validate YAML syntax first
            yaml.safe_load(config_content)
        except yaml.YAMLError as e:
            return {"error": f"Invalid YAML configuration: {e}"}

        try:
            result = self.analysis_chain.invoke({"config_content": config_content})
            return result
        except Exception as e:
            return {"error": f"Analysis failed: {e}"}
