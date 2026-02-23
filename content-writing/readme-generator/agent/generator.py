"""README generator — create project READMEs from project metadata."""
from __future__ import annotations
import os, json, re
from dataclasses import dataclass, field

BADGES = {
    "python": "![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)",
    "node": "![Node](https://img.shields.io/badge/Node.js-18+-green?logo=node.js)",
    "typescript": "![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue?logo=typescript)",
    "docker": "![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)",
    "mit": "![License: MIT](https://img.shields.io/badge/License-MIT-yellow)",
    "tests": "![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)",
}

@dataclass
class ProjectInfo:
    name: str
    description: str = ""
    language: str = ""
    license: str = "MIT"
    author: str = ""
    install_cmd: str = ""
    run_cmd: str = ""
    test_cmd: str = ""
    features: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    env_vars: list[str] = field(default_factory=list)
    api_endpoints: list[dict] = field(default_factory=list)
    contributing: bool = True
    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v}

def detect_project(directory: str) -> ProjectInfo:
    """Auto-detect project info from files."""
    info = ProjectInfo(name=os.path.basename(directory))
    if os.path.exists(os.path.join(directory, "package.json")):
        try:
            pkg = json.load(open(os.path.join(directory, "package.json")))
            info.name = pkg.get("name", info.name)
            info.description = pkg.get("description", "")
            info.language = "node"
            info.install_cmd = "npm install"
            info.run_cmd = "npm start"
            info.test_cmd = "npm test"
        except: pass
    elif os.path.exists(os.path.join(directory, "requirements.txt")):
        info.language = "python"
        info.install_cmd = "pip install -r requirements.txt"
        info.run_cmd = "python main.py"
        info.test_cmd = "pytest"
    elif os.path.exists(os.path.join(directory, "pyproject.toml")):
        info.language = "python"
        info.install_cmd = "pip install -e ."
        info.test_cmd = "pytest"
    if os.path.exists(os.path.join(directory, "Dockerfile")): info.prerequisites.append("Docker")
    if os.path.exists(os.path.join(directory, ".env.example")):
        try:
            for line in open(os.path.join(directory, ".env.example")):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    info.env_vars.append(line.split("=")[0])
        except: pass
    return info

def generate_readme(info: ProjectInfo) -> str:
    """Generate a README from project info."""
    lines = []
    # Title and badges
    lines.append(f"# {info.name}")
    badges = []
    if info.language in BADGES: badges.append(BADGES[info.language])
    if info.license and info.license.lower() in BADGES: badges.append(BADGES[info.license.lower()])
    if info.test_cmd: badges.append(BADGES["tests"])
    if badges: lines.append(" ".join(badges))
    lines.append("")
    if info.description:
        lines.extend([info.description, ""])
    # Features
    if info.features:
        lines.append("## ✨ Features")
        for f in info.features: lines.append(f"- {f}")
        lines.append("")
    # Prerequisites
    if info.prerequisites:
        lines.append("## 📋 Prerequisites")
        for p in info.prerequisites: lines.append(f"- {p}")
        lines.append("")
    # Install
    if info.install_cmd:
        lines.extend(["## 🚀 Quick Start", "```bash", info.install_cmd, "```", ""])
    if info.run_cmd:
        lines.extend(["## 🏃 Usage", "```bash", info.run_cmd, "```", ""])
    # Env vars
    if info.env_vars:
        lines.append("## 🔐 Environment Variables")
        lines.append("| Variable | Description |")
        lines.append("|----------|-------------|")
        for v in info.env_vars: lines.append(f"| `{v}` | TODO |")
        lines.append("")
    # API endpoints
    if info.api_endpoints:
        lines.append("## 📡 API Endpoints")
        for ep in info.api_endpoints:
            lines.append(f"- `{ep.get('method', 'GET')}` **{ep.get('path', '/')}** — {ep.get('description', '')}")
        lines.append("")
    # Testing
    if info.test_cmd:
        lines.extend(["## 🧪 Testing", "```bash", info.test_cmd, "```", ""])
    # Contributing
    if info.contributing:
        lines.extend(["## 🤝 Contributing", "1. Fork the repository", "2. Create a feature branch", "3. Commit your changes", "4. Push and create a PR", ""])
    # License
    if info.license:
        lines.extend([f"## 📄 License", f"This project is licensed under the {info.license} License.", ""])
    return "\n".join(lines)

def generate_from_template(name: str, template: str = "minimal") -> str:
    """Generate from a named template."""
    templates = {
        "minimal": ProjectInfo(name=name, description=f"{name} — a minimal project."),
        "api": ProjectInfo(name=name, description=f"{name} — a REST API.", language="node", features=["REST API", "Auth", "Database"], install_cmd="npm install", run_cmd="npm start", test_cmd="npm test"),
        "cli": ProjectInfo(name=name, description=f"{name} — a CLI tool.", language="python", features=["CLI interface", "Config support"], install_cmd="pip install -r requirements.txt", run_cmd="python main.py --help", test_cmd="pytest"),
    }
    info = templates.get(template, templates["minimal"])
    return generate_readme(info)
