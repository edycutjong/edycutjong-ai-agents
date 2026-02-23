"""Configuration for Deprecation Hunter."""

CONFIG = {
    "name": "deprecation-hunter",
    "version": "1.0.0",
    "description": "Find deprecated API usage in codebases",
    "ignore_patterns": [
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "dist",
        "build",
    ],
}
