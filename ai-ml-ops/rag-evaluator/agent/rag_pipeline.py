import os
from typing import List, Optional
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Import Config correctly
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import Config

class RAGPipeline:
    def __init__(self,
                 openai_api_key: str = None,
                 model_name: str = Config.DEFAULT_MODEL,
                 k: int = Config.DEFAULT_K):

        self.api_key = openai_api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API Key is required")

        self.model_name = model_name
        self.k = k
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.vectorstore = None
        self.retriever = None
        self.chain = None

    def index_documents(self, documents: List[Document]):
        """Indexes documents into ChromaDB."""
        # Use a temporary in-memory Chroma for this session to keep it simple and stateless per run if needed
        # Or persistent if configured. For now, let's go with ephemeral for the "agent" feel of fresh runs.
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": self.k})
        self.setup_chain()

    def setup_chain(self):
        """Sets up the RAG chain."""
        llm = ChatOpenAI(
            model=self.model_name,
            openai_api_key=self.api_key,
            temperature=0
        )

        template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
        prompt = ChatPromptTemplate.from_template(template)

        def format_docs(docs):
            return "\n\n".join([d.page_content for d in docs])

        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    def query(self, question: str) -> str:
        """Executes a query against the RAG pipeline."""
        if not self.chain:
            raise ValueError("Pipeline not initialized. Index documents first.")
        return self.chain.invoke(question)

    def retrieve_context(self, question: str) -> List[Document]:
        """Retrieves context documents for a question."""
        if not self.retriever:
            raise ValueError("Retriever not initialized.")
        return self.retriever.invoke(question)
