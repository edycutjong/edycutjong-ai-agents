import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def load_document(file_path: str) -> List[Document]:
    """Loads a document from a file path."""
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    return loader.load()

def split_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """Splits documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def ingest_file(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """High-level function to ingest a file and return split documents."""
    docs = load_document(file_path)
    split_docs = split_documents(docs, chunk_size, chunk_overlap)
    return split_docs
