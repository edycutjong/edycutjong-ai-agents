import os
import json
from click.testing import CliRunner
from main import cli
from lib.detector import detect_stack
from lib.env_scanner import scan_env_vars
from lib.ci_scanner import scan_ci_config
from lib.readme_parser import parse_readme

def test_cli_node_repo(mock_repo_node):
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", mock_repo_node, "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "Install Node.js" in data["prerequisites"][0]
    assert any("MY_PROD_TOKEN" in step for step in data["setup_steps"])
    assert any("API_KEY" in step for step in data["setup_steps"])
    assert any("npm i" in step for step in data["setup_steps"])
    assert any("npm run start" in step for step in data["verification_steps"])

def test_cli_python_repo(mock_repo_python):
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", mock_repo_python, "--format", "markdown"])
    assert result.exit_code == 0
    assert "Install Python" in result.output
    assert "make install" in result.output
    assert "make start" in result.output

def test_cli_terminal(mock_repo_node):
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", mock_repo_node, "--format", "terminal"])
    assert result.exit_code == 0
    assert "Developer Onboarding Checklist" in result.output

def test_detector_edge_cases(mock_repo_rust_go_java, mock_repo_overrides):
    stack1 = detect_stack(mock_repo_rust_go_java)
    assert "Rust" in stack1["languages"]
    assert "Go" in stack1["languages"]
    assert "Java" in stack1["languages"]
    assert "Docker Compose" in stack1["tools"]

    stack2 = detect_stack(mock_repo_overrides)
    assert "Python" in stack2["languages"]
    assert "Poetry/Pipenv/Hatch" in stack2["package_managers"]
    assert "Java/Kotlin" in stack2["languages"]

def test_cli_overrides(mock_repo_overrides):
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", mock_repo_overrides, "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["prerequisites"] == ["Custom pre-req"]
    assert data["setup_steps"] == ["Custom setup"]
    assert data["verification_steps"] == ["Custom verify"]

def test_empty_repo(tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", str(tmp_path), "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "Review repository documentation" in data["prerequisites"][0]
    
def test_malformed_package_json(tmp_path):
    (tmp_path / "package.json").write_text("{malformed", encoding="utf-8")
    stack = detect_stack(str(tmp_path))
    assert "JavaScript/TypeScript" in stack["languages"]
    assert "React" not in stack["frameworks"]

def test_gitlab_ci(tmp_path):
    (tmp_path / ".gitlab-ci.yml").write_text("stages:", encoding="utf-8")
    ci = scan_ci_config(str(tmp_path))
    assert "GitLab CI" in ci["ci_systems"]

def test_malformed_readme(tmp_path):
    # Test readme parser with a directory instead of file to trigger exception
    (tmp_path / "README.md").mkdir()
    readme_info = parse_readme(str(tmp_path))
    assert readme_info["setup_commands"] == []
    
def test_malformed_makefile(tmp_path):
    (tmp_path / "Makefile").mkdir()
    readme_info = parse_readme(str(tmp_path))
    assert readme_info["setup_commands"] == []

def test_malformed_ci(tmp_path):
    ci_dir = tmp_path / ".github" / "workflows"
    ci_dir.mkdir(parents=True)
    (ci_dir / "ci.yml").write_bytes(b'\x80\x81') # Invalid utf-8 triggers Exception
    ci = scan_ci_config(str(tmp_path))
    assert ci["secrets"] == []

def test_malformed_onboarding_yaml(tmp_path):
    (tmp_path / ".onboarding.yaml").write_text("{malformed:", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", str(tmp_path), "--format", "json"])
    assert result.exit_code == 0

def test_missing_onboarding_yaml(tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", str(tmp_path), "--format", "json"])
    assert result.exit_code == 0

def test_generate_checklist_fallbacks(mock_repo_rust_go_java):
    # This hits lines in generate_checklist for Go, Rust, Java
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", mock_repo_rust_go_java, "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert any("Install Go" in p for p in data["prerequisites"])
    assert any("Install Rust" in p for p in data["prerequisites"])
    assert any("cargo fetch" in p for p in data["setup_steps"])
    assert any("docker-compose up" in p for p in data["verification_steps"])
    
def test_generate_checklist_npm_pip_fallback(tmp_path):
    # No readme, so fallback is hit
    (tmp_path / "package.json").write_text('{"dependencies": {"react": "^18.0.0"}}', encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("requests==2.31.0", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", str(tmp_path), "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert any("npm install" in p for p in data["setup_steps"])
    assert any("pip install" in p for p in data["setup_steps"])
    assert any("npm start" in p for p in data["verification_steps"])
    
def test_import_error_tomli(monkeypatch, tmp_path):
    import builtins
    real_import = builtins.__import__
    def mock_import(name, *args, **kwargs):
        if name == "tomli":
            raise ImportError()
        return real_import(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", mock_import)
    
    # Reload module to trigger import error in try-except block
    import importlib
    from lib import detector
    importlib.reload(detector)
    
    (tmp_path / "pyproject.toml").write_text("[tool.poetry]", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", str(tmp_path), "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert any("pip install" in p for p in data["setup_steps"]) # fallbacks to pip since no tomli
    
    # Restore the detector module for other tests
    monkeypatch.undo()
    importlib.reload(detector)

def test_generate_checklist_default_kwargs(tmp_path):
    from lib.checklist import generate_checklist
    chk = generate_checklist(str(tmp_path))
    assert "prerequisites" in chk

def test_main_execution():
    import subprocess
    import sys
    # Runs the main block directly
    result = subprocess.run([sys.executable, "main.py", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
