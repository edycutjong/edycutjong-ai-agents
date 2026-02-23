"""Vector store management — FAISS for document embedding and retrieval."""

import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL


def create_vectorstore(documents: list[Document]) -> FAISS:
    """Create a FAISS vector store from documents.

    Args:
        documents: List of LangChain Document objects.

    Returns:
        FAISS vector store with embedded documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore


def load_and_embed_file(filepath: str) -> FAISS:
    """Load a file and create a vector store from its contents.

    Args:
        filepath: Path to the file (txt, md, or pdf).

    Returns:
        FAISS vector store.

    Raises:
        FileNotFoundError: If the file doesn't exist.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(filepath)
        text = "\n".join(page.extract_text() for page in reader.pages)
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

    docs = [Document(page_content=text, metadata={"source": filepath})]
    return create_vectorstore(docs)


def similarity_search(vectorstore: FAISS, query: str, k: int = 4) -> list[Document]:
    """Search for similar documents in the vector store.

    Args:
        vectorstore: FAISS vector store.
        query: Search query.
        k: Number of results to return.

    Returns:
        List of matching documents.
    """
    return vectorstore.similarity_search(query, k=k)
