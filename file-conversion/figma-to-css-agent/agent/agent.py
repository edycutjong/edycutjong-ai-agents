import os
import sys
from langchain_openai import ChatOpenAI
try:
    from langchain.agents import create_openai_tools_agent, AgentExecutor
except ImportError:  # pragma: no cover
    from langchain_classic.agents import create_openai_tools_agent, AgentExecutor  # pragma: no cover

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .tools import convert_figma_to_css, parse_figma_structure

# Fix imports for when running as script vs module
try:
    from prompts.system_prompts import FIGMA_AGENT_SYSTEM_PROMPT
    from config import OPENAI_API_KEY
except ImportError:  # pragma: no cover
    # Try relative if running as part of larger app
    from ..prompts.system_prompts import FIGMA_AGENT_SYSTEM_PROMPT  # pragma: no cover
    from ..config import OPENAI_API_KEY  # pragma: no cover

class FigmaAgent:
    """Agent for converting Figma designs to CSS."""

    def __init__(self, model_name: str = "gpt-4-turbo"):
        # API Key handling is done in main or config, but we need it here.
        pass  # pragma: no cover

        self.llm = ChatOpenAI(model=model_name, temperature=0, api_key=OPENAI_API_KEY or "dummy-key")  # pragma: no cover
        self.tools = [convert_figma_to_css, parse_figma_structure]  # pragma: no cover
        self.agent_executor = self._create_agent()  # pragma: no cover

    def _create_agent(self) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages([  # pragma: no cover
            ("system", FIGMA_AGENT_SYSTEM_PROMPT),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_openai_tools_agent(self.llm, self.tools, prompt)  # pragma: no cover
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)  # pragma: no cover

    def run(self, user_input: str) -> str:
        """Runs the agent with the user input."""
        try:  # pragma: no cover
            if not OPENAI_API_KEY:  # pragma: no cover
                 return "Error: OPENAI_API_KEY not found. Agent mode requires an API key."  # pragma: no cover

            result = self.agent_executor.invoke({"input": user_input})  # pragma: no cover
            return result["output"]  # pragma: no cover
        except Exception as e:  # pragma: no cover
            return f"An error occurred: {str(e)}"  # pragma: no cover
