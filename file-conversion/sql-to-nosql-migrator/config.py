"""Configuration for Sql To Nosql Migrator."""

import os

class config:
    """Settings for the SQL-to-NoSQL migrator."""
    name = "sql-to-nosql-migrator"
    version = "1.0.0"
    description = "Convert SQL schemas and queries to NoSQL equivalents"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "true").lower() == "true"

CONFIG = {
    "name": config.name,
    "version": config.version,
    "description": config.description,
    "ignore_patterns": [
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "dist",
        "build",
    ],
}
