import os
from jinja2 import Environment, FileSystemLoader
from typing import List, Dict, Any, Union

class Generator:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def _map_type(self, type_str: str) -> Dict[str, str]:
        mapping = {
            "str": {"sql_type": "String(255)", "api_type": "string"},
            "int": {"sql_type": "Integer", "api_type": "integer"},
            "float": {"sql_type": "Float", "api_type": "number"},
            "bool": {"sql_type": "Boolean", "api_type": "boolean"},
            "datetime": {"sql_type": "DateTime", "api_type": "string"}
        }
        return mapping.get(type_str, {"sql_type": "String(255)", "api_type": "string"})

    def generate(self, schema: List[Dict[str, str]], csv_data: Union[str, bytes] = None) -> Dict[str, Union[str, bytes]]:
        # Enrich schema with mapped types
        enriched_schema = []
        for col in schema:
            types = self._map_type(col['type'])
            enriched_schema.append({
                **col,
                **types
            })

        files = {}
        templates = ['app.py.j2', 'models.py.j2', 'database.py.j2', 'requirements.txt.j2', 'readme.md.j2']

        for tmpl_name in templates:
            template = self.env.get_template(tmpl_name)
            content = template.render(columns=enriched_schema)
            # Remove .j2 extension
            out_name = tmpl_name[:-3]
            files[out_name] = content

        if csv_data:
            files['data.csv'] = csv_data

        return files
