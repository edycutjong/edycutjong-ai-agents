import json
import uuid
from typing import Dict, Any
from agent.parser import OpenAPIParser

class PostmanExporter:
    def __init__(self, parser: OpenAPIParser):
        self.parser = parser

    def export(self) -> Dict[str, Any]:
        info = self.parser.specification.get('info', {})
        collection = {
            "info": {
                "_postman_id": str(uuid.uuid4()),
                "name": info.get('title', 'Exported API'),
                "description": info.get('description', ''),
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "item": []
        }

        paths = self.parser.get_paths()
        for path in paths:
            methods = self.parser.get_methods_for_path(path)
            for method in methods:
                item = self._create_item(path, method)
                collection['item'].append(item)

        return collection

    def _create_item(self, path: str, method: str) -> Dict[str, Any]:
        operation = self.parser.get_operation(path, method)
        summary = operation.get('summary', f"{method} {path}")

        # Handle path variables: /users/{id} -> :id
        path_segments = path.strip('/').split('/')
        formatted_segments = []
        for segment in path_segments:
            if segment.startswith('{') and segment.endswith('}'):
                formatted_segments.append(':' + segment[1:-1])
            else:
                formatted_segments.append(segment)

        request = {
            "method": method.upper(),
            "header": [],
            "url": {
                "raw": "{{base_url}}/" + "/".join(formatted_segments),
                "host": ["{{base_url}}"],
                "path": formatted_segments
            }
        }

        return {
            "name": summary,
            "request": request,
            "response": []
        }
