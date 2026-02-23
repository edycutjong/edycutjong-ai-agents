"""Configuration for Css Dead Code Remover."""

CONFIG = {
    "name": "css-dead-code-remover",
    "version": "1.0.0",
    "description": "Find and remove unused CSS selectors from stylesheets",
    "ignore_patterns": [
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "dist",
        "build",
    ],
}
