"""Tests for Config File Generator."""
import sys, os, json, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import (
    generate_config, generate_multiple, list_config_types,
    list_presets, detect_project_type, TEMPLATES,
)

# --- Generation Tests ---

def test_generate_eslint_default():
    result = generate_config("eslint", "default")
    assert result["filename"] == ".eslintrc.json"
    content = json.loads(result["content"])
    assert "rules" in content

def test_generate_eslint_react():
    result = generate_config("eslint", "react")
    content = json.loads(result["content"])
    assert "react" in content["plugins"]

def test_generate_eslint_typescript():
    result = generate_config("eslint", "typescript")
    content = json.loads(result["content"])
    assert "@typescript-eslint" in content["plugins"]

def test_generate_prettier():
    result = generate_config("prettier", "default")
    content = json.loads(result["content"])
    assert content["singleQuote"] is True
    assert content["tabWidth"] == 2

def test_generate_tsconfig():
    result = generate_config("tsconfig", "default")
    content = json.loads(result["content"])
    assert content["compilerOptions"]["strict"] is True

def test_generate_tsconfig_nextjs():
    result = generate_config("tsconfig", "nextjs")
    content = json.loads(result["content"])
    assert content["compilerOptions"]["jsx"] == "preserve"

def test_generate_editorconfig():
    result = generate_config("editorconfig", "default")
    assert "root = true" in result["content"]
    assert "indent_style = space" in result["content"]

def test_generate_gitignore_node():
    result = generate_config("gitignore", "node")
    assert "node_modules/" in result["content"]
    assert ".env" in result["content"]

def test_generate_gitignore_python():
    result = generate_config("gitignore", "python")
    assert "__pycache__/" in result["content"]
    assert ".venv/" in result["content"]

def test_generate_dockerfile_node():
    result = generate_config("dockerfile", "node")
    assert "FROM node:20-alpine" in result["content"]
    assert "npm ci" in result["content"]

def test_generate_dockerfile_python():
    result = generate_config("dockerfile", "python")
    assert "FROM python:3.12-slim" in result["content"]

def test_generate_github_actions_node():
    result = generate_config("github-actions", "node")
    assert "npm test" in result["content"]

def test_generate_github_actions_python():
    result = generate_config("github-actions", "python")
    assert "pytest" in result["content"]

# --- Error Handling ---

def test_unknown_type():
    result = generate_config("nonexistent")
    assert "error" in result

def test_unknown_preset():
    result = generate_config("eslint", "nonexistent")
    assert "error" in result

# --- Overrides ---

def test_overrides():
    result = generate_config("prettier", "default", overrides={"tabWidth": 4})
    content = json.loads(result["content"])
    assert content["tabWidth"] == 4

# --- Listing ---

def test_list_config_types():
    types = list_config_types()
    assert len(types) >= 7
    names = [t["type"] for t in types]
    assert "eslint" in names
    assert "prettier" in names

def test_list_presets():
    presets = list_presets("eslint")
    assert "default" in presets
    assert "react" in presets

# --- Multiple Generation ---

def test_generate_multiple():
    results = generate_multiple(["eslint", "prettier"])
    assert len(results) == 2
    assert all("error" not in r for r in results)

# --- Project Detection ---

def test_detect_node():
    assert detect_project_type(["package.json", "index.js"]) == "node"

def test_detect_nextjs():
    assert detect_project_type(["package.json", "next.config.js"]) == "nextjs"

def test_detect_python():
    assert detect_project_type(["requirements.txt", "main.py"]) == "python"

def test_detect_rust():
    assert detect_project_type(["Cargo.toml", "src"]) == "rust"

def test_detect_unknown():
    assert detect_project_type(["random.file"]) == "unknown"
