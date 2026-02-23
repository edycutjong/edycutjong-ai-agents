import os
import sys
import pytest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.ingestion import load_document, split_documents, ingest_file
from langchain_core.documents import Document

def test_load_document_txt(tmp_path):
    # Create a dummy text file
    f = tmp_path / "test.txt"
    f.write_text("This is a test document.")

    docs = load_document(str(f))
    assert len(docs) == 1
    assert docs[0].page_content == "This is a test document."

def test_load_document_unsupported(tmp_path):
    f = tmp_path / "test.xyz"
    f.write_text("content")

    with pytest.raises(ValueError, match="Unsupported file type"):
        load_document(str(f))

def test_split_documents():
    doc = Document(page_content="A" * 2000)
    docs = split_documents([doc], chunk_size=1000, chunk_overlap=0)
    assert len(docs) == 2
    assert len(docs[0].page_content) == 1000

@patch("agent.ingestion.load_document")
@patch("agent.ingestion.split_documents")
def test_ingest_file(mock_split, mock_load):
    mock_load.return_value = [Document(page_content="test")]
    mock_split.return_value = [Document(page_content="test")]

    result = ingest_file("dummy.txt")

    mock_load.assert_called_once_with("dummy.txt")
    mock_split.assert_called_once()
    assert len(result) == 1
