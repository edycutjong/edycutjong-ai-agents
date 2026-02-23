from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import sys

# Ensure parent directory is in path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class DebuggerAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        if self.api_key:
            try:
                self.llm = ChatOpenAI(api_key=self.api_key, model="gpt-4o")
            except Exception:
                self.llm = None
        else:
            self.llm = None

        self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts")

    def _load_prompt(self, filename):
        try:
            with open(os.path.join(self.prompts_dir, filename), "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return "You are an expert OAuth 2.0 debugger."

    def analyze_error(self, error_message, context=None):
        if not self.llm:
            return "AI Analysis unavailable: OpenAI API Key missing."

        system_prompt = self._load_prompt("error_analysis.txt")
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Error: {error}\nContext: {context}")
        ])

        chain = prompt | self.llm | StrOutputParser()

        try:
            return chain.invoke({"error": error_message, "context": context or "No additional context."})
        except Exception as e:
            return f"Error during analysis: {str(e)}"

    def analyze_configuration(self, config_data):
        if not self.llm:
            return "AI Analysis unavailable: OpenAI API Key missing."

        system_prompt = self._load_prompt("config_review.txt")
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Configuration: {config}")
        ])

        chain = prompt | self.llm | StrOutputParser()

        try:
            return chain.invoke({"config": config_data})
        except Exception as e:
            return f"Error during analysis: {str(e)}"
