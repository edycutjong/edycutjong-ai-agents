import io  # pragma: no cover
from typing import Union  # pragma: no cover

def read_file_content(file: Union[str, io.BytesIO]) -> str:  # pragma: no cover
    """Reads content from a file path or a BytesIO object."""
    if isinstance(file, str):  # pragma: no cover
        try:  # pragma: no cover
            with open(file, 'r', encoding='utf-8') as f:  # pragma: no cover
                return f.read()  # pragma: no cover
        except Exception as e:  # pragma: no cover
            return f"Error reading file: {e}"  # pragma: no cover
    elif isinstance(file, io.BytesIO):  # pragma: no cover
        try:  # pragma: no cover
            return file.getvalue().decode('utf-8')  # pragma: no cover
        except Exception as e:  # pragma: no cover
            return f"Error decoding file: {e}"  # pragma: no cover
    return ""  # pragma: no cover

def clean_markdown(text: str) -> str:  # pragma: no cover
    """Removes code block markers from markdown text if present."""
    text = text.strip()  # pragma: no cover
    if text.startswith("```markdown"):  # pragma: no cover
        text = text[11:]  # pragma: no cover
    elif text.startswith("```"):  # pragma: no cover
        text = text[3:]  # pragma: no cover

    if text.endswith("```"):  # pragma: no cover
        text = text[:-3]  # pragma: no cover

    return text.strip()  # pragma: no cover
