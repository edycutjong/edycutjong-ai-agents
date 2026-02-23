import json
from typing import Optional
from langchain.tools import tool
from .parser import FigmaParser
from .generator import CSSGenerator

@tool
def convert_figma_to_css(json_content: str, format: str = "css") -> str:
    """
    Parses Figma JSON content and generates CSS code.

    Args:
        json_content (str): The raw JSON string from Figma.
        format (str): The desired output format ("css", "scss", "css-in-js"). Defaults to "css".

    Returns:
        str: The generated CSS/SCSS/JS code.
    """
    try:
        data = json.loads(json_content)
        parser = FigmaParser(data)
        processed_nodes = parser.parse()

        generator = CSSGenerator(processed_nodes)

        if format.lower() == "scss":
            return generator.generate_scss()
        elif format.lower() == "css-in-js":
            return generator.generate_css_in_js()
        else:
            return generator.generate_css()

    except json.JSONDecodeError:
        return "Error: Invalid JSON content provided."
    except Exception as e:
        return f"Error during conversion: {str(e)}"

@tool
def parse_figma_structure(json_content: str) -> str:
    """
    Parses Figma JSON and returns a summary of the structure (nodes found).
    Useful for understanding the document before generating CSS.

    Args:
        json_content (str): The raw JSON string from Figma.

    Returns:
        str: Summary of processed nodes.
    """
    try:
        data = json.loads(json_content)
        parser = FigmaParser(data)
        processed_nodes = parser.parse()

        summary = [f"- {node['name']} ({node['type']})" for node in processed_nodes]
        return "Found nodes:\n" + "\n".join(summary)

    except Exception as e:
        return f"Error parsing structure: {str(e)}"
