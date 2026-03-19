import pytest
import tempfile
import os
import yaml

@pytest.fixture
def mock_repo(monkeypatch):
    from git import Repo
    class MockRepo:
        def __init__(self, *args, **kwargs):
            self.working_dir = "/mock/repo"
        class MockCommit:
            def __init__(self):
                self.author = type("Author", (), {"email": "test@example.com"})
                self.stats = type("Stats", (), {"files": {"src/main.py": 10, "README.md": 2}})
        def commit(self, *args, **kwargs):
            return self.MockCommit()
        def is_dirty(self):
            return False
            
    monkeypatch.setattr("git.Repo", MockRepo)

@pytest.fixture
def test_config_file():
    config_data = {
        "criticality": {
            "paths": {
                "^src/auth/": 10.0,
                "\\.(yml|yaml)$": 5.0,
                "\\.md$": 1.0,
                "^tests/": 0.0
            },
            "weight": 0.3
        },
        "blast_radius": {
            "high_threshold_files": 10,
            "weight": 0.3
        },
        "test_coverage": {
            "gap_penalty": 20.0,
            "weight": 0.2
        },
        "history": {
            "weight": 0.2,
            "familiarity_bonus_max": 15.0
        },
        "thresholds": {
            "fail_ci_score": 75
        }
    }
    
    fd, path = tempfile.mkstemp(suffix=".yaml")
    with os.fdopen(fd, 'w') as f:
        yaml.dump(config_data, f)
        
    yield path
    os.remove(path)
