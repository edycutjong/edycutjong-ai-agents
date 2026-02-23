"""Configuration for Vuln Auto Patcher."""

CONFIG = {
    "name": "vuln-auto-patcher",
    "version": "1.0.0",
    "description": "Auto-patch known vulnerabilities in dependencies",
    "ignore_patterns": [
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "dist",
        "build",
    ],
}
