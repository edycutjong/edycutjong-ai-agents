import os
import json
from unittest.mock import patch, mock_open
from agent.generator import detect_project, ProjectInfo, generate_readme

def test_detect_project_invalid_package_json():
    # Simulate existing package.json that is not valid JSON
    with patch("os.path.exists") as mock_exists:
        # Check package.json exists
        mock_exists.side_effect = lambda path: "package.json" in path
        m = mock_open(read_data="{invalid_json")
        with patch("builtins.open", m):
            info = detect_project("test_dir")
            assert info.language == ""

def test_detect_project_pyproject_toml():
    with patch("os.path.exists") as mock_exists:
        def exists_side_effect(path):
            return "pyproject.toml" in path
        mock_exists.side_effect = exists_side_effect
        info = detect_project("test_dir")
        assert info.language == "python"
        assert info.install_cmd == "pip install -e ."

def test_detect_project_env_example():
    with patch("os.path.exists") as mock_exists:
        def exists_side_effect(path):
            return ".env.example" in path
        mock_exists.side_effect = exists_side_effect
        
        m = mock_open(read_data="API_KEY=secret\n# comment\nINVALID_LINE\n")
        with patch("builtins.open", m):
            info = detect_project("test_dir")
            assert "API_KEY" in info.env_vars
            assert len(info.env_vars) == 1

def test_detect_project_env_example_error():
    with patch("os.path.exists") as mock_exists:
        def exists_side_effect(path):
            return ".env.example" in path
        mock_exists.side_effect = exists_side_effect
        
        # Simulate open raising an exception
        with patch("builtins.open", side_effect=IOError):
            info = detect_project("test_dir")
            assert len(info.env_vars) == 0

def test_generate_readme_prerequisites():
    info = ProjectInfo(name="Test", prerequisites=["Node 18+", "Redis"])
    readme = generate_readme(info)
    assert "## 📋 Prerequisites" in readme
    assert "- Node 18+" in readme
    assert "- Redis" in readme
