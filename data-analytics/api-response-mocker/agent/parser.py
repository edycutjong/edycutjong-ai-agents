from prance import ResolvingParser
from typing import Dict, Any, List, Optional

class OpenAPIParser:
    def __init__(self, spec_content: str):
        self.spec_content = spec_content
        self.parser = self._create_parser()

    def _create_parser(self) -> ResolvingParser:
        try:
            # ResolvingParser handles $ref resolution automatically
            return ResolvingParser(spec_string=self.spec_content, backend='openapi-spec-validator')
        except Exception as e:
            # Fallback or specific error handling could go here
            raise ValueError(f"Failed to parse OpenAPI spec: {e}")

    @property
    def specification(self) -> Dict[str, Any]:
        return self.parser.specification

    def get_paths(self) -> List[str]:
        return list(self.specification.get('paths', {}).keys())

    def get_methods_for_path(self, path: str) -> List[str]:
        path_item = self.specification.get('paths', {}).get(path, {})
        methods = []
        for method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
            if method in path_item:
                methods.append(method.upper())
        return methods

    def get_operation(self, path: str, method: str) -> Dict[str, Any]:
        return self.specification.get('paths', {}).get(path, {}).get(method.lower())

    def get_response_schema(self, path: str, method: str, status_code: str = '200') -> Optional[Dict[str, Any]]:
        operation = self.get_operation(path, method)
        if not operation:
            return None

        responses = operation.get('responses', {})
        # Try exact match first (handling both string '200' and int 200 keys)
        response = responses.get(status_code)
        if not response:
            try:
                response = responses.get(int(status_code))
            except (ValueError, TypeError):
                pass

        if not response:
            # Fallback to 'default' or first 2xx
            if 'default' in responses:
                response = responses['default']
            else:
                for code, resp in responses.items():
                    if str(code).startswith('2'):
                        response = resp
                        break

        if not response:
            return None

        content = response.get('content', {})
        # Prioritize application/json
        json_content = content.get('application/json')
        if not json_content:
            # fallback to first content type
            if content:
                json_content = list(content.values())[0]

        if json_content:
            return json_content.get('schema')
        return None
