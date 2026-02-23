from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

try:
    from ..config import config
    from ..prompts.templates import (
        GRAPHQL_TYPES_PROMPT,
        GRAPHQL_OPERATIONS_PROMPT,
        RESOLVER_GENERATOR_PROMPT,
        MIGRATION_GUIDE_PROMPT
    )
except ImportError:
    # Fallback for when running as a script or with different path setup
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from config import config
    from prompts.templates import (
        GRAPHQL_TYPES_PROMPT,
        GRAPHQL_OPERATIONS_PROMPT,
        RESOLVER_GENERATOR_PROMPT,
        MIGRATION_GUIDE_PROMPT
    )

class GraphQLGenerator:
    """Generates GraphQL artifacts using an LLM."""

    def __init__(self, api_key: str = None):
        api_key = api_key or config.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OpenAI API Key is required.")

        self.llm = ChatOpenAI(
            model=config.MODEL_NAME,
            temperature=0.2, # Low temperature for consistent code generation
            openai_api_key=api_key
        )

    def generate_types(self, schemas: Dict[str, Any], api_summary: str) -> str:
        """Generates GraphQL Type Definitions."""
        chain = GRAPHQL_TYPES_PROMPT | self.llm | StrOutputParser()
        return chain.invoke({
            "schemas": str(schemas),
            "api_summary": api_summary
        })

    def generate_operations(self, endpoints: Dict[str, Any], api_summary: str, existing_types: str) -> str:
        """Generates GraphQL Query and Mutation Types."""
        chain = GRAPHQL_OPERATIONS_PROMPT | self.llm | StrOutputParser()
        return chain.invoke({
            "endpoints": str(endpoints),
            "api_summary": api_summary,
            "existing_types": existing_types
        })

    def generate_resolvers(self, schema_sdl: str, endpoints: Dict[str, Any], language: str = "python") -> str:
        """Generates Resolvers code."""
        chain = RESOLVER_GENERATOR_PROMPT | self.llm | StrOutputParser()
        return chain.invoke({
            "language": language,
            "schema_sdl": schema_sdl,
            "endpoints": str(endpoints)
        })

    def generate_migration_guide(self, schema_sdl: str, endpoints: Dict[str, Any], api_summary: str) -> str:
        """Generates a Migration Guide."""
        chain = MIGRATION_GUIDE_PROMPT | self.llm | StrOutputParser()
        return chain.invoke({
            "api_summary": api_summary,
            "schema_sdl": schema_sdl,
            "endpoints": str(endpoints)
        })
