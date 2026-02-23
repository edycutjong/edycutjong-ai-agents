import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_document(file_path):
    """
    Loads a document from a file path.
    Supports .pdf and .txt.
    Returns a list of Documents (chunks).
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
        pages = loader.load()
    elif ext == ".txt":
        loader = TextLoader(file_path)
        pages = loader.load()
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    return pages

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Splits documents into smaller chunks for processing.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)
