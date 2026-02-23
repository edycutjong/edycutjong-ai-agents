import os
import sys
from langchain_openai import ChatOpenAI
try:
    from langchain.agents import create_openai_tools_agent, AgentExecutor
except ImportError:
    from langchain_classic.agents import create_openai_tools_agent, AgentExecutor

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .tools import convert_figma_to_css, parse_figma_structure

# Fix imports for when running as script vs module
try:
    from prompts.system_prompts import FIGMA_AGENT_SYSTEM_PROMPT
    from config import OPENAI_API_KEY
except ImportError:
    # Try relative if running as part of larger app
    from ..prompts.system_prompts import FIGMA_AGENT_SYSTEM_PROMPT
    from ..config import OPENAI_API_KEY

class FigmaAgent:
    """Agent for converting Figma designs to CSS."""

    def __init__(self, model_name: str = "gpt-4-turbo"):
        # API Key handling is done in main or config, but we need it here.
        pass

        self.llm = ChatOpenAI(model=model_name, temperature=0, api_key=OPENAI_API_KEY or "dummy-key")
        self.tools = [convert_figma_to_css, parse_figma_structure]
        self.agent_executor = self._create_agent()

    def _create_agent(self) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages([
            ("system", FIGMA_AGENT_SYSTEM_PROMPT),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def run(self, user_input: str) -> str:
        """Runs the agent with the user input."""
        try:
            if not OPENAI_API_KEY:
                 return "Error: OPENAI_API_KEY not found. Agent mode requires an API key."

            result = self.agent_executor.invoke({"input": user_input})
            return result["output"]
        except Exception as e:
            return f"An error occurred: {str(e)}"
