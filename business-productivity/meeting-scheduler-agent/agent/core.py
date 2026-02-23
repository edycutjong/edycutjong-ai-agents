from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from datetime import datetime
import os
import sys

# Ensure imports work regardless of execution context
try:
    from .llm import get_llm
    from .tools import get_tools
    from ..prompts.system_prompts import SYSTEM_PROMPT
except (ImportError, ValueError):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.append(root_dir)

    from agent.llm import get_llm
    from agent.tools import get_tools
    from prompts.system_prompts import SYSTEM_PROMPT

def create_agent_executor():
    llm = get_llm()
    tools = get_tools()

    if llm is None:
        return None

    # Format system prompt with current time
    # Note: This time is fixed at agent creation. Ideally, use a callable modifier for dynamic time.
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    formatted_system_prompt = SYSTEM_PROMPT.format(current_time=current_time)

    checkpointer = MemorySaver()
    agent = create_react_agent(llm, tools, state_modifier=formatted_system_prompt, checkpointer=checkpointer)
    return agent

def run_agent_step(agent_executor, user_input: str, thread_id: str = "default"):
    """
    Runs a single step of the agent with the user input.
    """
    try:
        if agent_executor is None:
            return "Agent not initialized (check API Key)."

        config = {"configurable": {"thread_id": thread_id}}

        # Invoke with the new user message
        # The agent will append this to the history stored in checkpointer
        response = agent_executor.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config
        )

        # The last message is the AI's response
        return response["messages"][-1].content
    except Exception as e:
        return f"Error running agent: {str(e)}"
