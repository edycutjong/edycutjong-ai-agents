import os
import sys

# Ensure the parent directory is in sys.path to allow imports if run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from agent.tools import (
    research_tool,
    calculator_tool,
    accommodation_tool,
    dining_tool,
)
from config import OPENAI_API_KEY, MODEL_NAME
from prompts.templates import SYSTEM_PROMPT

class TravelAgent:
    def __init__(self):
        if not OPENAI_API_KEY:
            self.llm = None
        else:
            self.llm = ChatOpenAI(model=MODEL_NAME, temperature=0.7)

        self.tools = [research_tool, calculator_tool, accommodation_tool, dining_tool]

        if self.llm:
            # create_react_agent returns a CompiledGraph
            # We can pass the system prompt as state_modifier
            self.agent_executor = create_react_agent(self.llm, self.tools, state_modifier=SYSTEM_PROMPT)
        else:
            self.agent_executor = None

    def generate_itinerary(self, destination: str, dates: str) -> str:
        if not self.agent_executor:
            return "Error: OPENAI_API_KEY not found. Please set it in .env or environment variables."

        user_input = f"Plan a trip to {destination} for the dates {dates}. Please provide the complete itinerary in Markdown."

        try:
            # LangGraph expects messages list or dict with messages
            result = self.agent_executor.invoke({"messages": [HumanMessage(content=user_input)]})
            # result["messages"] contains the conversation history. The last message is the AI response.
            return result["messages"][-1].content
        except Exception as e:
            return f"An error occurred while generating the itinerary: {e}"
