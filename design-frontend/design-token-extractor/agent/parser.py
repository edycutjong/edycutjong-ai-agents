import json
from typing import Union, Dict

class DesignParser:
    @staticmethod
    def parse_content(content: str, file_type: str) -> str:
        """
        Parses the content of a file based on its type.
        Returns a string representation suitable for LLM processing.
        """
        if file_type.lower() in ['json', 'figma']:
            try:
                data = json.loads(content)
                # Pretty print JSON for better LLM comprehension
                return json.dumps(data, indent=2)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON content")
        elif file_type.lower() in ['md', 'markdown', 'txt', 'text']:
            return content
        else:
            # Fallback to just returning the content string
            return content
