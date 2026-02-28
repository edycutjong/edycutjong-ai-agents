from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
import os
from utils.config import config

class AIHelper:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.llm = ChatOpenAI(temperature=0.7, openai_api_key=self.api_key)
        else:
            self.llm = None

    def explain_rule(self, rule_code: str, description: str) -> str:
        """Explains a style rule using AI."""
        if not self.llm:
            return f"Rule {rule_code}: {description}. (Mocked AI explanation: This rule helps keep code readable.)"

        prompt = PromptTemplate(
            input_variables=["rule_code", "description", "tone"],
            template="You are a {tone} coding assistant. Explain the Python style rule '{rule_code}: {description}' and why it is important. Keep it brief."
        )

        try:
            chain = prompt | self.llm
            response = chain.invoke({"rule_code": rule_code, "description": description, "tone": config.tone})
            return response.content
        except Exception as e:
            return f"Error explaining rule: {e}"

    def check_vibe(self, code_snippet: str) -> str:
        """Checks the 'vibe' of the code (readability, complexity, naming)."""
        if not self.llm:
            return "The code looks okay! (Mocked AI vibe check)"

        prompt = PromptTemplate(
            input_variables=["code", "tone"],
            template="You are a {tone} coding assistant. Analyze the following code snippet for its 'vibe' - is it clean, pythonic, or messy? Give a short, fun assessment.\n\nCode:\n{code}"
        )

        try:
            chain = prompt | self.llm
            response = chain.invoke({"code": code_snippet, "tone": config.tone})
            return response.content
        except Exception as e:
            return f"Error checking vibe: {e}"

    def learn_from_codebase(self, file_content: str) -> str:
        """Learns patterns from a file (mocked for now as simple analysis)."""
        # In a real agent, this might update a vector store or fine-tune context
        if not self.llm:
             return "I've analyzed this file and learned its style! (Mocked)"

        prompt = PromptTemplate(
            input_variables=["code"],
            template="Analyze this code file and summarize the coding style (indentation, naming conventions, docstrings).\n\nCode:\n{code}"
        )

        try:
            chain = prompt | self.llm
            # Truncate content to avoid token limits in this simple implementation
            truncated_content = file_content[:2000]
            response = chain.invoke({"code": truncated_content})
            return response.content
        except Exception as e:
            return f"Error learning from code: {e}"

ai_helper = AIHelper()
