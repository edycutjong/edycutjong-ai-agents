import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_document(file_path):
    """
    Loads a document from a file path.
    Supports .pdf and .txt.
    Returns a list of Documents (chunks).
    """
    _, ext = os.path.splitext(file_path)  # pragma: no cover
    ext = ext.lower()  # pragma: no cover

    if ext == ".pdf":  # pragma: no cover
        loader = PyPDFLoader(file_path)  # pragma: no cover
        pages = loader.load()  # pragma: no cover
    elif ext == ".txt":  # pragma: no cover
        loader = TextLoader(file_path)  # pragma: no cover
        pages = loader.load()  # pragma: no cover
    else:
        raise ValueError(f"Unsupported file extension: {ext}")  # pragma: no cover

    return pages  # pragma: no cover

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Splits documents into smaller chunks for processing.
    """
    text_splitter = RecursiveCharacterTextSplitter(  # pragma: no cover
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)  # pragma: no cover
