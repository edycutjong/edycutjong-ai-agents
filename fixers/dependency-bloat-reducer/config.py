"""Configuration for Dependency Bloat Reducer."""

CONFIG = {
    "name": "dependency-bloat-reducer",
    "version": "1.0.0",
    "description": "Analyze and reduce dependency bloat in projects",
    "ignore_patterns": [
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "dist",
        "build",
    ],
}
