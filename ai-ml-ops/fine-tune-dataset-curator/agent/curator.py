import sys
import os

# Add the project root to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from agent.tools import DATASET_TOOLS
from prompts.system import SYSTEM_PROMPT
from config import Config

def create_curator_agent():
    """
    Creates and returns the Curator Agent executor.
    """
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=Config.OPENAI_API_KEY
    )

    # Define the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent
    agent = create_openai_tools_agent(llm, DATASET_TOOLS, prompt)

    # Create the executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=DATASET_TOOLS,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent_executor
