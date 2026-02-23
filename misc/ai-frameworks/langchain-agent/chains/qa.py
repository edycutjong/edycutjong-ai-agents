"""Q&A chain for document question-answering."""

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import MODEL_NAME, TEMPERATURE


def create_qa_chain() -> LLMChain:
    """Create a chain for document Q&A.

    Returns:
        LLMChain configured for Q&A with context.
    """
    llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""Answer the question based on the provided context. 
If the answer is not in the context, say "I don't have enough information to answer this."

Context:
{context}

Question: {question}

Answer:""",
    )

    return LLMChain(llm=llm, prompt=prompt)
