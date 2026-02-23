"""Tests for Boilerplate Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import generate_project, write_project, list_templates, slugify, format_project_markdown, TEMPLATES

def test_list_templates():
    templates = list_templates()
    assert len(templates) >= 5
    assert "python-cli" in templates

def test_slugify():
    assert slugify("My App") == "my-app"
    assert slugify("hello_world") == "hello-world"

def test_generate_python_cli():
    p = generate_project("My Tool", "python-cli")
    assert p.name == "My Tool"
    assert "main.py" in p.files
    assert "My Tool" in p.files["main.py"]

def test_generate_python_package():
    p = generate_project("my pkg", "python-package")
    assert "src/my-pkg/__init__.py" in p.files

def test_generate_express():
    p = generate_project("My API", "express-api")
    assert "index.js" in p.files
    assert "package.json" in p.files

def test_generate_fastapi():
    p = generate_project("FastApp", "fastapi")
    assert "app/main.py" in p.files
    assert "FastApp" in p.files["app/main.py"]

def test_generate_flask():
    p = generate_project("FlaskApp", "flask")
    assert "app.py" in p.files

def test_unknown_template():
    with pytest.raises(ValueError):
        generate_project("x", "nonexistent")

def test_write_project(tmp_path):
    p = generate_project("Test", "python-cli")
    created = write_project(p, str(tmp_path))
    assert len(created) > 0
    assert os.path.exists(os.path.join(str(tmp_path), "main.py"))

def test_files_have_content():
    p = generate_project("Demo", "python-cli")
    for filepath, content in p.files.items():
        if filepath.endswith(".py") and "__init__" not in filepath:
            assert len(content) > 0

def test_gitignore_included():
    for template in TEMPLATES:
        p = generate_project("Test", template)
        assert ".gitignore" in p.files

def test_readme_included():
    for template in TEMPLATES:
        p = generate_project("Test", template)
        assert "README.md" in p.files

def test_to_dict():
    p = generate_project("Test", "python-cli")
    d = p.to_dict()
    assert d["name"] == "Test"
    assert "files" in d

def test_format_markdown():
    p = generate_project("Test", "python-cli")
    md = format_project_markdown(p)
    assert "Test" in md
    assert "python-cli" in md
