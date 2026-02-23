import io
from typing import Union

def read_file_content(file: Union[str, io.BytesIO]) -> str:
    """Reads content from a file path or a BytesIO object."""
    if isinstance(file, str):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
    elif isinstance(file, io.BytesIO):
        try:
            return file.getvalue().decode('utf-8')
        except Exception as e:
            return f"Error decoding file: {e}"
    return ""

def clean_markdown(text: str) -> str:
    """Removes code block markers from markdown text if present."""
    text = text.strip()
    if text.startswith("```markdown"):
        text = text[11:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()
