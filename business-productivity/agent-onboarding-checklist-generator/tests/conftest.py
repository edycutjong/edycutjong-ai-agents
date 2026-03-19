import pytest

@pytest.fixture
def mock_repo_node(tmp_path):
    repo = tmp_path / "node_repo"
    repo.mkdir()
    (repo / "package.json").write_text('{"dependencies": {"react": "^18.0.0", "next": "13", "express": "4", "vue": "3", "svelte": "4"}}', encoding="utf-8")
    (repo / ".env.example").write_text("API_KEY=123 # The main API key\nDB_PASS=", encoding="utf-8")
    readme_content = "```bash\nnpm i\nnpm run start\n```"
    (repo / "README.md").write_text(readme_content, encoding="utf-8")
    ci_dir = repo / ".github" / "workflows"
    ci_dir.mkdir(parents=True)
    (ci_dir / "ci.yml").write_text("env:\n  TOKEN: ${{ secrets.MY_PROD_TOKEN }}", encoding="utf-8")
    return str(repo)

@pytest.fixture
def mock_repo_python(tmp_path):
    repo = tmp_path / "python_repo"
    repo.mkdir()
    (repo / "requirements.txt").write_text("requests==2.31.0", encoding="utf-8")
    (repo / "Makefile").write_text("install:\n\tpip install -r requirements.txt\nstart:\n\tpython main.py\n", encoding="utf-8")
    (repo / "Dockerfile").write_text("FROM python:3.11", encoding="utf-8")
    (repo / ".env.template").write_text("SECRET=\n", encoding="utf-8")
    return str(repo)

@pytest.fixture
def mock_repo_rust_go_java(tmp_path):
    repo = tmp_path / "mixed_repo"
    repo.mkdir()
    (repo / "Cargo.toml").write_text("[package]", encoding="utf-8")
    (repo / "go.mod").write_text("module example", encoding="utf-8")
    (repo / "pom.xml").write_text("<project></project>", encoding="utf-8")
    (repo / "docker-compose.yml").write_text("version: '3'", encoding="utf-8")
    return str(repo)

@pytest.fixture
def mock_repo_overrides(tmp_path):
    repo = tmp_path / "overrides_repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[tool.poetry]", encoding="utf-8")
    (repo / "build.gradle_kts").write_text('plugins { java }', encoding="utf-8")
    (repo / "build.gradle").write_text("apply plugin: 'java'", encoding="utf-8")
    (repo / ".onboarding.yaml").write_text("prerequisites:\n  - Custom pre-req\nsetup_steps:\n  - Custom setup\nverification_steps:\n  - Custom verify", encoding="utf-8")
    return str(repo)
