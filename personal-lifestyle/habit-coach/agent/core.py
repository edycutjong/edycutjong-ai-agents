import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
try:
    from langchain.agents import AgentExecutor, create_tool_calling_agent
except ImportError:
    try:
        from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
    except ImportError:
        # Fallback or error
        raise ImportError("Could not import AgentExecutor or create_tool_calling_agent from langchain or langchain_classic")

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
try:
    from .tools import add_new_habit, log_completion, get_habit_list, get_habit_stats
except ImportError:
    import sys
    sys.path.append(os.path.dirname(__file__))
    from tools import add_new_habit, log_completion, get_habit_list, get_habit_stats

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """You are a supportive and motivational Habit Coach.
Your goal is to help users build and maintain positive habits.
You can track their progress, log completions, and provide analytics.

When interacting with the user:
1. Be encouraging and positive.
2. If they mention a new habit, offer to add it.
3. If they mention completing something, log it for today.
4. If they ask for progress, show them their stats.
5. Analyze their patterns (e.g., "You tend to skip Gym on Mondays") based on the stats provided.

If a tool fails or returns an error, explain it clearly to the user.
Always confirm actions (e.g., "I've logged your Run for today!").
"""

def get_agent_executor():
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    tools = [add_new_habit, log_completion, get_habit_list, get_habit_stats]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor
