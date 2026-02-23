"""Boilerplate generator — scaffold project structures for various frameworks."""
from __future__ import annotations
import os, json
from dataclasses import dataclass, field

TEMPLATES = {
    "python-cli": {
        "description": "Python CLI application",
        "files": {
            "main.py": '#!/usr/bin/env python3\n"""Main entry point."""\nimport argparse\n\ndef main():\n    parser = argparse.ArgumentParser(description="{name}")\n    parser.add_argument("--version", action="version", version="1.0.0")\n    args = parser.parse_args()\n    print("Hello from {name}!")\n\nif __name__ == "__main__":\n    main()\n',
            "requirements.txt": "",
            "README.md": "# {name}\n\n## Quick Start\n```bash\npip install -r requirements.txt\npython main.py\n```\n",
            ".gitignore": ".venv/\n__pycache__/\n*.pyc\n.env\n",
            "tests/__init__.py": "",
            "tests/test_main.py": 'import pytest\n\ndef test_placeholder():\n    assert True\n',
        },
    },
    "python-package": {
        "description": "Python package with setup",
        "files": {
            "src/{slug}/__init__.py": '__version__ = "0.1.0"\n',
            "src/{slug}/core.py": '"""Core module."""\n\ndef hello(name: str = "World") -> str:\n    return f"Hello, {{name}}!"\n',
            "tests/__init__.py": "",
            "tests/test_core.py": 'from {slug}.core import hello\n\ndef test_hello():\n    assert hello() == "Hello, World!"\n',
            "pyproject.toml": '[build-system]\nrequires = ["setuptools>=68.0"]\nbuild-backend = "setuptools.backends._legacy:_Backend"\n\n[project]\nname = "{slug}"\nversion = "0.1.0"\nrequires-python = ">=3.9"\n',
            "README.md": "# {name}\n\n## Install\n```bash\npip install -e .\n```\n",
            ".gitignore": ".venv/\n__pycache__/\n*.pyc\n*.egg-info/\ndist/\n",
        },
    },
    "express-api": {
        "description": "Express.js REST API",
        "files": {
            "index.js": 'const express = require("express");\nconst app = express();\napp.use(express.json());\n\napp.get("/", (req, res) => res.json({{ message: "Hello from {name}!" }}));\napp.get("/health", (req, res) => res.json({{ status: "ok" }}));\n\nconst PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log(`Server running on port ${{PORT}}`));\n',
            "package.json": '{{\n  "name": "{slug}",\n  "version": "1.0.0",\n  "main": "index.js",\n  "scripts": {{\n    "start": "node index.js",\n    "dev": "nodemon index.js",\n    "test": "jest"\n  }},\n  "dependencies": {{\n    "express": "^4.18.0"\n  }}\n}}\n',
            "README.md": "# {name}\n\n```bash\nnpm install && npm start\n```\n",
            ".gitignore": "node_modules/\n.env\n",
        },
    },
    "fastapi": {
        "description": "FastAPI application",
        "files": {
            "app/main.py": 'from fastapi import FastAPI\n\napp = FastAPI(title="{name}")\n\n@app.get("/")\ndef root():\n    return {{"message": "Hello from {name}!"}}\n\n@app.get("/health")\ndef health():\n    return {{"status": "ok"}}\n',
            "app/__init__.py": "",
            "requirements.txt": "fastapi>=0.100.0\nuvicorn[standard]>=0.23.0\n",
            "README.md": "# {name}\n\n```bash\npip install -r requirements.txt\nuvicorn app.main:app --reload\n```\n",
            ".gitignore": ".venv/\n__pycache__/\n*.pyc\n.env\n",
            "tests/__init__.py": "",
            "tests/test_main.py": 'from fastapi.testclient import TestClient\nfrom app.main import app\n\nclient = TestClient(app)\n\ndef test_root():\n    r = client.get("/")\n    assert r.status_code == 200\n',
        },
    },
    "flask": {
        "description": "Flask web application",
        "files": {
            "app.py": 'from flask import Flask, jsonify\n\napp = Flask(__name__)\n\n@app.route("/")\ndef index():\n    return jsonify(message="Hello from {name}!")\n\nif __name__ == "__main__":\n    app.run(debug=True)\n',
            "requirements.txt": "flask>=3.0.0\npytest\n",
            "README.md": "# {name}\n\n```bash\npip install -r requirements.txt\npython app.py\n```\n",
            ".gitignore": ".venv/\n__pycache__/\n*.pyc\n.env\n",
        },
    },
}

@dataclass
class GeneratedProject:
    name: str
    template: str
    files: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"name": self.name, "template": self.template, "files": list(self.files.keys())}

def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("_", "-")

def generate_project(name: str, template: str, extra_vars: dict | None = None) -> GeneratedProject:
    """Generate a project from a template."""
    tmpl = TEMPLATES.get(template)
    if not tmpl:
        raise ValueError(f"Unknown template: {template}. Available: {', '.join(TEMPLATES.keys())}")
    slug = slugify(name)
    variables = {"name": name, "slug": slug, **(extra_vars or {})}
    project = GeneratedProject(name=name, template=template)
    for filepath, content in tmpl["files"].items():
        resolved_path = filepath.format(**variables)
        resolved_content = content.format(**variables) if content else ""
        project.files[resolved_path] = resolved_content
    return project

def write_project(project: GeneratedProject, output_dir: str) -> list[str]:
    """Write generated project files to disk."""
    created = []
    for filepath, content in project.files.items():
        full_path = os.path.join(output_dir, filepath)
        os.makedirs(os.path.dirname(full_path) or output_dir, exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        created.append(filepath)
    return created

def list_templates() -> dict:
    return {k: v["description"] for k, v in TEMPLATES.items()}

def format_project_markdown(project: GeneratedProject) -> str:
    lines = [f"# Generated: {project.name}", f"**Template:** {project.template}", f"**Files:** {len(project.files)}", ""]
    for f in sorted(project.files.keys()):
        lines.append(f"- `{f}`")
    return "\n".join(lines)
