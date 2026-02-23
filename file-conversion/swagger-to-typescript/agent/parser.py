import yaml
import httpx
from pathlib import Path
from typing import Dict, Any

def load_swagger(source: str) -> Dict[str, Any]:
    """
    Loads a Swagger/OpenAPI spec from a file path or URL.

    Args:
        source (str): The file path or URL to the Swagger spec.

    Returns:
        Dict[str, Any]: The parsed Swagger spec.
    """
    content = ""

    if source.startswith("http://") or source.startswith("https://"):
        try:
            response = httpx.get(source)
            response.raise_for_status()
            content = response.text
        except httpx.HTTPError as e:
            raise ValueError(f"Failed to fetch Swagger from URL: {e}")
    else:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {source}")
        content = path.read_text(encoding="utf-8")

    try:
        # yaml.safe_load handles both JSON and YAML
        return yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValueError(f"Failed to parse Swagger file: {e}")
