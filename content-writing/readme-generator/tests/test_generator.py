"""Tests for README Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import ProjectInfo, generate_readme, generate_from_template, detect_project

def test_basic():
    info = ProjectInfo(name="MyApp", description="A cool app")
    md = generate_readme(info)
    assert "# MyApp" in md
    assert "A cool app" in md

def test_badges():
    info = ProjectInfo(name="App", language="python", test_cmd="pytest")
    md = generate_readme(info)
    assert "Python" in md

def test_features():
    info = ProjectInfo(name="App", features=["Fast", "Secure"])
    md = generate_readme(info)
    assert "Fast" in md and "Secure" in md

def test_install():
    info = ProjectInfo(name="App", install_cmd="npm install")
    md = generate_readme(info)
    assert "npm install" in md

def test_env_vars():
    info = ProjectInfo(name="App", env_vars=["API_KEY", "DB_URL"])
    md = generate_readme(info)
    assert "API_KEY" in md

def test_api_endpoints():
    info = ProjectInfo(name="App", api_endpoints=[{"method": "GET", "path": "/users", "description": "List users"}])
    md = generate_readme(info)
    assert "/users" in md

def test_contributing():
    info = ProjectInfo(name="App", contributing=True)
    md = generate_readme(info)
    assert "Contributing" in md

def test_license():
    info = ProjectInfo(name="App", license="MIT")
    md = generate_readme(info)
    assert "MIT" in md

def test_template_minimal():
    md = generate_from_template("MyApp", "minimal")
    assert "# MyApp" in md

def test_template_api():
    md = generate_from_template("MyAPI", "api")
    assert "REST API" in md

def test_template_cli():
    md = generate_from_template("MyCLI", "cli")
    assert "CLI" in md

def test_detect_python(tmp_path):
    (tmp_path / "requirements.txt").write_text("flask")
    info = detect_project(str(tmp_path))
    assert info.language == "python"

def test_detect_node(tmp_path):
    (tmp_path / "package.json").write_text('{"name":"test","description":"A test"}')
    info = detect_project(str(tmp_path))
    assert info.language == "node"

def test_detect_docker(tmp_path):
    (tmp_path / "requirements.txt").write_text("")
    (tmp_path / "Dockerfile").write_text("FROM python")
    info = detect_project(str(tmp_path))
    assert "Docker" in info.prerequisites

def test_to_dict():
    info = ProjectInfo(name="X", language="python")
    d = info.to_dict()
    assert d["name"] == "X"
