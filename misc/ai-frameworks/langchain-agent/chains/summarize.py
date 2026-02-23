"""Summarization chain for condensing documents."""

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import MODEL_NAME, TEMPERATURE


def create_summarize_chain() -> LLMChain:
    """Create a chain for document summarization.

    Returns:
        LLMChain configured for summarization.
    """
    llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Summarize the following text in a clear, structured format.
Include:
1. A one-sentence TL;DR
2. Key points (bullet list)
3. Important details or numbers

Text to summarize:
{text}

Summary:""",
    )

    return LLMChain(llm=llm, prompt=prompt)
