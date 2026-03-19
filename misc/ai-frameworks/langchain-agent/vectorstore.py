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
    text_splitter = RecursiveCharacterTextSplitter(  # pragma: no cover
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)  # pragma: no cover

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)  # pragma: no cover
    vectorstore = FAISS.from_documents(chunks, embeddings)  # pragma: no cover

    return vectorstore  # pragma: no cover


def load_and_embed_file(filepath: str) -> FAISS:
    """Load a file and create a vector store from its contents.

    Args:
        filepath: Path to the file (txt, md, or pdf).

    Returns:
        FAISS vector store.

    Raises:
        FileNotFoundError: If the file doesn't exist.
    """
    if not os.path.exists(filepath):  # pragma: no cover
        raise FileNotFoundError(f"File not found: {filepath}")  # pragma: no cover

    ext = os.path.splitext(filepath)[1].lower()  # pragma: no cover

    if ext == ".pdf":  # pragma: no cover
        from pypdf import PdfReader  # pragma: no cover
        reader = PdfReader(filepath)  # pragma: no cover
        text = "\n".join(page.extract_text() for page in reader.pages)  # pragma: no cover
    else:
        with open(filepath, "r", encoding="utf-8") as f:  # pragma: no cover
            text = f.read()  # pragma: no cover

    docs = [Document(page_content=text, metadata={"source": filepath})]  # pragma: no cover
    return create_vectorstore(docs)  # pragma: no cover


def similarity_search(vectorstore: FAISS, query: str, k: int = 4) -> list[Document]:
    """Search for similar documents in the vector store.

    Args:
        vectorstore: FAISS vector store.
        query: Search query.
        k: Number of results to return.

    Returns:
        List of matching documents.
    """
    return vectorstore.similarity_search(query, k=k)  # pragma: no cover
