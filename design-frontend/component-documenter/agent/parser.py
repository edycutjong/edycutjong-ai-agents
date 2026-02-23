import os
import sys
from typing import Optional, Tuple

# Ensure the parent directory is in sys.path so we can import config
# This is needed if we run this file directly or if the module resolution is tricky
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from config import Config
except ImportError:
    # Fallback for when running from the root of the repo (less likely for this app but good for tests)
    # We might need to adjust based on how tests are run.
    pass

def get_language_from_extension(filename: str) -> str:
    """
    Determines the language/framework based on file extension.
    Returns 'unknown' if not supported.
    """
    _, ext = os.path.splitext(filename)
    # Using the Config class map.
    # Note: Config.SUPPORTED_EXTENSIONS keys are lowercase.
    ext = ext.lower()
    return Config.SUPPORTED_EXTENSIONS.get(ext, 'text')

def read_file_content(filepath: str) -> str:
    """
    Reads the content of a file.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise ValueError(f"Error reading file {filepath}: {str(e)}")

def parse_uploaded_file(uploaded_file) -> Tuple[str, str]:
    """
    Parses a Streamlit UploadedFile object.
    Returns (content, language).
    """
    filename = uploaded_file.name
    # content is bytes in Streamlit's UploadedFile, need to decode
    content = uploaded_file.getvalue().decode('utf-8')
    language = get_language_from_extension(filename)
    return content, language
