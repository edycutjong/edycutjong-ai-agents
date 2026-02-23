"""Research chain for multi-step topic investigation."""

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import MODEL_NAME, TEMPERATURE


def create_research_chain() -> LLMChain:
    """Create a chain for in-depth research analysis.

    Returns:
        LLMChain configured for research tasks.
    """
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0.3)

    prompt = PromptTemplate(
        input_variables=["topic", "search_results"],
        template="""You are a research analyst. Based on the search results below, 
create a comprehensive analysis of the topic.

Topic: {topic}

Search Results:
{search_results}

Create a structured report with:
## Executive Summary
(2-3 sentences)

## Key Findings
(bullet points)

## Analysis
(detailed discussion)

## Recommendations
(actionable next steps)

Report:""",
    )

    return LLMChain(llm=llm, prompt=prompt)
