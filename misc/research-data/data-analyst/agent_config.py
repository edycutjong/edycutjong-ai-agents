import os
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

def create_agent(df, model_name="gpt-4o"):
    """
    Creates a Pandas DataFrame agent.

    Args:
        df: The pandas DataFrame to analyze.
        model_name: The name of the OpenAI model to use.

    Returns:
        An agent executor capable of answering questions about the DataFrame.
    """

    llm = ChatOpenAI(
        model=model_name,
        temperature=0
    )

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True, # Required to execute Python code for analysis
        agent_type="openai-tools",
    )

    return agent
