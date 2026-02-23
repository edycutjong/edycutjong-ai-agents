from langchain_openai import ChatOpenAI
import os
import sys

# Add parent directory to path to import config
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config import Config
from .analyzer import CIAnalyzer
from .optimizer import CIOptimizer

class CIAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        if self.api_key:
            self.llm = ChatOpenAI(
                model=Config.MODEL_NAME,
                temperature=Config.TEMPERATURE,
                api_key=self.api_key
            )
            self.analyzer = CIAnalyzer(self.llm)
            self.optimizer = CIOptimizer(self.llm)
        else:
            self.llm = None
            self.analyzer = CIAnalyzer(None)
            self.optimizer = CIOptimizer(None)

    def analyze(self, config_content: str) -> dict:
        return self.analyzer.analyze(config_content)

    def optimize(self, config_content: str, analysis_result: dict) -> str:
        return self.optimizer.optimize(config_content, analysis_result)
