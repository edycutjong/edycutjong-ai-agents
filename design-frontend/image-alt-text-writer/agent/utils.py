import base64
import requests
import os
from io import BytesIO

def encode_image(image_path: str) -> str:
    """Encodes a local image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return None

def get_image_data(src: str, base_path: str = None) -> str:
    """
    Returns base64 encoded image data.
    If src is a URL, downloads it.
    If src is a local path, reads it.
    """
    if src.startswith(('http://', 'https://')):
        try:
            response = requests.get(src, timeout=10)
            response.raise_for_status()
            return base64.b64encode(response.content).decode('utf-8')
        except Exception as e:
            print(f"Failed to download image {src}: {e}")
            return None
    else:
        # Local file
        if base_path:
            # Handle potential relative paths carefully
            full_path = os.path.join(base_path, src)
        else:
            full_path = src

        if os.path.exists(full_path):
            return encode_image(full_path)
        else:
            print(f"Image not found: {full_path}")
            return None
