import os
import webvtt

def read_file(file_path: str) -> str:
    """
    Reads a file and returns its content as a string.
    Supports .txt and .vtt files.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.vtt':
        return _read_vtt(file_path)
    else:
        # Default to treating as text
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

def _read_vtt(file_path: str) -> str:
    """
    Parses a VTT file and extracts the text content.
    """
    vtt = webvtt.read(file_path)
    transcript = []
    for caption in vtt:
        transcript.append(caption.text)
    return "\n".join(transcript)
