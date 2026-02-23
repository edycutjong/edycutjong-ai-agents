"""Configuration for Unused Asset Cleaner."""

CONFIG = {
    "name": "unused-asset-cleaner",
    "version": "1.0.0",
    "description": "Find and remove unused assets (images, fonts, etc) from projects",
    "ignore_patterns": [
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "dist",
        "build",
    ],
}
