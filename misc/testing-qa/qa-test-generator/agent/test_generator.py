from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import json
import sys

# Ensure the parent directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try importing from the same directory structure first
try:
    from prompts.system_prompts import SCENARIO_GENERATION_PROMPT, PLAYWRIGHT_CODE_GENERATION_PROMPT, SELF_HEALING_PROMPT
except ImportError:
    # If not found, rely on sys.path modification above
    from system_prompts import SCENARIO_GENERATION_PROMPT, PLAYWRIGHT_CODE_GENERATION_PROMPT, SELF_HEALING_PROMPT

class TestGenerator:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-4-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        self.llm = None
        if self.api_key:
            self.llm = ChatOpenAI(api_key=self.api_key, model=self.model_name, temperature=0.7)
        else:
            print("Warning: No OpenAI API Key provided. Test generation will not work with LLM.")

    def generate_scenarios(self, ui_elements: List[Dict], context_description: str = "") -> List[str]:
        """
        Generates a list of test scenarios based on UI elements.
        """
        if not self.llm:
            return ["Mock Scenario 1: Verify page load", "Mock Scenario 2: Check button click"]

        # Convert UI elements to a simplified string representation
        elements_str = json.dumps([el for el in ui_elements], indent=2)

        prompt = ChatPromptTemplate.from_messages([
            ("system", SCENARIO_GENERATION_PROMPT),
            ("user", "Context: {context}\n\nUI Elements:\n{elements}\n\nGenerate a list of test scenarios.")
        ])

        chain = prompt | self.llm | StrOutputParser()

        response = chain.invoke({
            "context": context_description,
            "elements": elements_str
        })

        # Parse the response into a list (assuming LLM returns a list format)
        # For simplicity, we split by newlines and filter empty lines
        scenarios = [line.strip() for line in response.split('\n') if line.strip()]
        return scenarios

    def generate_playwright_code(self, scenarios: List[str], url: str, ui_structure: str) -> str:
        """
        Generates Playwright test code for the given scenarios.
        """
        if not self.llm:
            return self._mock_playwright_code(url)

        scenarios_str = "\n".join(scenarios)

        prompt = ChatPromptTemplate.from_messages([
            ("system", PLAYWRIGHT_CODE_GENERATION_PROMPT),
            ("user", "Target URL: {url}\n\nPage Structure (HTML snippet):\n{structure}\n\nTest Scenarios:\n{scenarios}\n\nWrite the Python code for these tests. Ensure you handle waits and assertions correctly.")
        ])

        chain = prompt | self.llm | StrOutputParser()

        code = chain.invoke({
            "url": url,
            "structure": ui_structure[:10000], # Truncate to avoid context limits if necessary
            "scenarios": scenarios_str
        })

        return self._clean_code_block(code)

    def self_heal(self, error_log: str, existing_code: str) -> str:
        """
        Analyzes an error log and the existing code to suggest a fix.
        """
        if not self.llm:
            return "# Mock fix: " + existing_code

        prompt = ChatPromptTemplate.from_messages([
            ("system", SELF_HEALING_PROMPT),
            ("user", "Error Log:\n{error}\n\nExisting Code:\n{code}\n\nProvide the corrected code block.")
        ])

        chain = prompt | self.llm | StrOutputParser()

        fixed_code = chain.invoke({
            "error": error_log,
            "code": existing_code
        })

        return self._clean_code_block(fixed_code)

    def _clean_code_block(self, text: str) -> str:
        """
        Removes markdown code block delimiters.
        """
        if "```python" in text:
            text = text.split("```python")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return text.strip()

    def _mock_playwright_code(self, url: str) -> str:
        return f"""
import pytest
import re
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def page_fixture(page: Page):
    page.goto("{url}")
    yield page

def test_page_title(page_fixture):
    expect(page_fixture).to_have_title(re.compile(".*"))

def test_example_interaction(page_fixture):
    # This is a mock test generated without LLM
    assert True
"""
