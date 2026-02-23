import json
import yaml
from typing import Dict, Any, Union

class OpenAPIParser:
    """Parses OpenAPI/Swagger specifications (JSON or YAML)."""

    def __init__(self, spec_content: str):
        self.spec_content = spec_content
        self.spec_data = self._parse_content()

    def _parse_content(self) -> Dict[str, Any]:
        """Parses the raw content into a dictionary."""
        try:
            data = json.loads(self.spec_content)
        except json.JSONDecodeError:
            try:
                data = yaml.safe_load(self.spec_content)
            except yaml.YAMLError:
                raise ValueError("Invalid specification format. Must be JSON or YAML.")

        if not isinstance(data, dict):
            raise ValueError("Invalid specification format. Content must parse to a dictionary.")

        return data

    def get_info(self) -> Dict[str, Any]:
        """Returns the API information."""
        return self.spec_data.get("info", {})

    def get_paths(self) -> Dict[str, Any]:
        """Returns the paths (endpoints) definition."""
        return self.spec_data.get("paths", {})

    def get_components(self) -> Dict[str, Any]:
        """Returns the components (schemas, parameters, etc.)."""
        return self.spec_data.get("components", {}) or self.spec_data.get("definitions", {})

    def get_schemas(self) -> Dict[str, Any]:
        """Returns the schema definitions."""
        components = self.get_components()
        return components.get("schemas", {}) or components # Fallback for Swagger 2.0 definitions

    def summarize(self) -> str:
        """Returns a summary of the API for the LLM context."""
        info = self.get_info()
        paths = self.get_paths()
        schemas = self.get_schemas()

        summary = f"API Title: {info.get('title', 'Unknown')}\n"
        summary += f"Description: {info.get('description', 'No description')}\n"
        summary += f"Version: {info.get('version', 'Unknown')}\n\n"

        summary += "Endpoints:\n"
        for path, methods in paths.items():
            for method, details in methods.items():
                summary += f"- {method.upper()} {path}: {details.get('summary', 'No summary')}\n"

        summary += "\nSchemas:\n"
        for schema_name, schema_def in schemas.items():
             summary += f"- {schema_name}: {schema_def.get('type', 'object')}\n"

        return summary

    def get_full_spec(self) -> Dict[str, Any]:
        """Returns the full parsed specification."""
        return self.spec_data
