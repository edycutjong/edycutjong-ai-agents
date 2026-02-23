from typing import Dict, Any, Optional

try:
    from .parser import OpenAPIParser
    from .generator import GraphQLGenerator
except ImportError:
    from parser import OpenAPIParser
    from generator import GraphQLGenerator

class RestToGraphqlConverter:
    """Orchestrates the conversion from REST to GraphQL."""

    def __init__(self, api_key: str = None):
        self.generator = GraphQLGenerator(api_key=api_key)

    def convert(self, spec_content: str, language: str = "python") -> Dict[str, str]:
        """
        Converts a REST API specification to GraphQL artifacts.

        Args:
            spec_content: The OpenAPI/Swagger spec content (JSON/YAML).
            language: The target language for resolvers (default: python).

        Returns:
            A dictionary containing:
            - schema: The full GraphQL SDL.
            - resolvers: The generated resolver code.
            - migration_guide: The migration guide markdown.
        """
        # 1. Parse the spec
        parser = OpenAPIParser(spec_content)
        api_summary = parser.summarize()
        schemas = parser.get_schemas()
        endpoints = parser.get_paths()

        # 2. Generate GraphQL Types
        graphql_types = self.generator.generate_types(schemas, api_summary)

        # 3. Generate Operations (Query/Mutation)
        graphql_operations = self.generator.generate_operations(endpoints, api_summary, graphql_types)

        # 4. Combine Schema
        full_schema = f"{graphql_types}\n\n{graphql_operations}"

        # 5. Generate Resolvers
        resolvers = self.generator.generate_resolvers(full_schema, endpoints, language)

        # 6. Generate Migration Guide
        migration_guide = self.generator.generate_migration_guide(full_schema, endpoints, api_summary)

        return {
            "schema": full_schema,
            "resolvers": resolvers,
            "migration_guide": migration_guide
        }
