"""Main agent setup with tools, memory, and reasoning."""

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory

from tools import create_search_tool, create_calculator_tool, create_file_reader_tool
from config import MODEL_NAME, TEMPERATURE, MAX_ITERATIONS, MAX_MEMORY_MESSAGES, MEMORY_KEY


def create_agent() -> AgentExecutor:
    """Create a LangChain agent with tools and conversational memory.

    Returns:
        Configured AgentExecutor.
    """
    # Initialize LLM
    llm = ChatOpenAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        streaming=True,
    )

    # Create tools
    tools = [
        create_search_tool(),
        create_calculator_tool(),
        create_file_reader_tool(),
    ]

    # Create prompt with memory
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI research assistant. You can:
1. Search the web for current information
2. Perform mathematical calculations
3. Read and analyze files

When answering questions:
- Use tools when you need real-time data or calculations
- Think step by step for complex questions
- Cite your sources when possible
- Be concise but thorough
- If you're unsure, say so rather than guessing"""),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create memory
    memory = ConversationBufferWindowMemory(
        memory_key=MEMORY_KEY,
        return_messages=True,
        k=MAX_MEMORY_MESSAGES,
    )

    # Create agent
    agent = create_openai_tools_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        max_iterations=MAX_ITERATIONS,
        verbose=False,
        handle_parsing_errors=True,
    )
