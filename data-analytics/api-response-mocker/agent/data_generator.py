from typing import Any, Dict, Optional, List
from faker import Faker
import random
import os

class DataGenerator:
    def __init__(self, use_llm: bool = False, openai_api_key: Optional[str] = None):
        self.faker = Faker()
        self.use_llm = use_llm
        self.openai_api_key = openai_api_key

    def generate_from_schema(self, schema: Dict[str, Any], field_name: Optional[str] = None) -> Any:
        """
        Generate data based on the JSON schema.
        """
        if not schema:
            return {}

        schema_type = schema.get('type')

        # Handle 'oneOf', 'anyOf', 'allOf' if necessary. For now, take first of oneOf/anyOf
        if 'oneOf' in schema:
            return self.generate_from_schema(schema['oneOf'][0], field_name)
        if 'anyOf' in schema:
            return self.generate_from_schema(schema['anyOf'][0], field_name)

        if schema_type == 'object':
            return self._generate_object(schema)
        elif schema_type == 'array':
            return self._generate_array(schema, field_name)
        elif schema_type == 'string':
            return self._generate_string(schema, field_name)
        elif schema_type == 'integer':
            return self._generate_integer(schema)
        elif schema_type == 'number':
            return self._generate_number(schema)
        elif schema_type == 'boolean':
            return self.faker.boolean()
        else:
            # Maybe implicit object if properties exist
            if 'properties' in schema:
                return self._generate_object(schema)
            return None

    def _generate_object(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        properties = schema.get('properties', {})
        result = {}
        for key, prop_schema in properties.items():
            result[key] = self.generate_from_schema(prop_schema, field_name=key)
        return result

    def _generate_array(self, schema: Dict[str, Any], field_name: Optional[str] = None) -> List[Any]:
        items_schema = schema.get('items', {})
        min_items = schema.get('minItems', 1)
        max_items = schema.get('maxItems', 3)
        count = random.randint(min_items, max_items)
        return [self.generate_from_schema(items_schema, field_name) for _ in range(count)]

    def _generate_string(self, schema: Dict[str, Any], field_name: Optional[str] = None) -> str:
        fmt = schema.get('format')
        if fmt == 'email':
            return self.faker.email()
        elif fmt == 'uuid':
            return self.faker.uuid4()
        elif fmt == 'date-time':
            return self.faker.iso8601()
        elif fmt == 'date':
            return self.faker.date()
        elif fmt == 'uri' or fmt == 'url':
            return self.faker.url()
        elif 'enum' in schema:
            return random.choice(schema['enum'])

        # Heuristic based on field name
        if field_name:
            fname = field_name.lower()
            if 'name' in fname:
                return self.faker.name()
            if 'phone' in fname:
                return self.faker.phone_number()
            if 'address' in fname:
                return self.faker.address()
            if 'city' in fname:
                return self.faker.city()
            if 'country' in fname:
                return self.faker.country()
            if 'job' in fname or 'title' in fname:
                return self.faker.job()
            if 'color' in fname:
                return self.faker.color_name()
            if 'description' in fname or 'bio' in fname:
                return self.faker.sentence()
            if 'user' in fname or 'username' in fname:
                return self.faker.user_name()

        return self.faker.word()

    def _generate_integer(self, schema: Dict[str, Any]) -> int:
        minimum = schema.get('minimum', 0)
        maximum = schema.get('maximum', 1000)
        return random.randint(minimum, maximum)

    def _generate_number(self, schema: Dict[str, Any]) -> float:
        minimum = schema.get('minimum', 0.0)
        maximum = schema.get('maximum', 1000.0)
        return random.uniform(minimum, maximum)
