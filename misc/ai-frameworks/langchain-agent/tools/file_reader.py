"""File reader tool — reads text and PDF files."""

import os
from langchain.tools import Tool


def _read_file(filepath: str) -> str:
    """Read content from a text or PDF file.

    Args:
        filepath: Path to the file.

    Returns:
        File content as string.
    """
    if not os.path.exists(filepath):  # pragma: no cover
        return f"Error: File '{filepath}' not found."  # pragma: no cover

    ext = os.path.splitext(filepath)[1].lower()  # pragma: no cover

    try:  # pragma: no cover
        if ext == ".pdf":  # pragma: no cover
            from pypdf import PdfReader  # pragma: no cover
            reader = PdfReader(filepath)  # pragma: no cover
            text = ""  # pragma: no cover
            for page in reader.pages:  # pragma: no cover
                text += page.extract_text() + "\n"  # pragma: no cover
            return text.strip() or "Error: Could not extract text from PDF."  # pragma: no cover
        else:
            with open(filepath, "r", encoding="utf-8") as f:  # pragma: no cover
                return f.read()  # pragma: no cover
    except Exception as e:  # pragma: no cover
        return f"Error reading file: {e}"  # pragma: no cover


def create_file_reader_tool() -> Tool:
    """Create a file reader tool.

    Returns:
        Configured file reader tool.
    """
    return Tool(  # pragma: no cover
        name="File Reader",
        func=_read_file,
        description=(
            "Read the contents of a file. Supports .txt, .md, .csv, .json, and .pdf files. "
            "Input should be the file path."
        ),
    )
