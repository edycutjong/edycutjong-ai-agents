import os
import re
from typing import Optional

def clean_text(text: str) -> str:
    """Cleans up text by removing extra whitespace and stripping."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def save_to_file(content: str, filename: str, format: str = "md") -> str:
    """Saves content to a file with the given format."""
    if not filename.endswith(f".{format}"):
        filename = f"{filename}.{format}"

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return filename

def format_filename(title: str) -> str:
    """Formats a title into a valid filename (slug)."""
    # Remove non-alphanumeric characters (keep spaces and dashes)
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    # Replace spaces with dashes
    slug = re.sub(r'\s+', '-', slug)
    return slug.lower()
