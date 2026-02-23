"""Configuration for Api Breaking Change Detect."""

CONFIG = {
    "name": "api-breaking-change-detect",
    "version": "1.0.0",
    "description": "Detect breaking changes in API endpoints by comparing OpenAPI specs",
    "ignore_patterns": [
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "dist",
        "build",
    ],
}
