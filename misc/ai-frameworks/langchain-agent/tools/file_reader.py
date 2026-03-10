"""File reader tool — reads text and PDF files."""

import os
from langchain_core.tools import Tool


def _read_file(filepath: str) -> str:
    """Read content from a text or PDF file.

    Args:
        filepath: Path to the file.

    Returns:
        File content as string.
    """
    if not os.path.exists(filepath):
        return f"Error: File '{filepath}' not found."

    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == ".pdf":
            from pypdf import PdfReader
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip() or "Error: Could not extract text from PDF."
        else:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


def create_file_reader_tool() -> Tool:
    """Create a file reader tool.

    Returns:
        Configured file reader tool.
    """
    return Tool(
        name="File Reader",
        func=_read_file,
        description=(
            "Read the contents of a file. Supports .txt, .md, .csv, .json, and .pdf files. "
            "Input should be the file path."
        ),
    )
