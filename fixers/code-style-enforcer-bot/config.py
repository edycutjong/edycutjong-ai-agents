"""Configuration for Code Style Enforcer Bot."""

CONFIG = {  # pragma: no cover
    "name": "code-style-enforcer-bot",
    "version": "1.0.0",
    "description": "Enforce consistent code style across a project",
    "ignore_patterns": [
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "dist",
        "build",
    ],
}
