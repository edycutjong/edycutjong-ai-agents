"""Configuration for Doc Drift Fixer."""

CONFIG = {
    "name": "doc-drift-fixer",
    "version": "1.0.0",
    "description": "Detect and fix documentation drift from source code",
    "ignore_patterns": [
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "dist",
        "build",
    ],
}
