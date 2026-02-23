import os
import json
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from tools.analyzer import DependencyAnalyzer

@pytest.fixture
def temp_project(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    package_json = {
        "dependencies": {"react": "^16.8.0"},
        "devDependencies": {"jest": "^26.0.0"},
        "scripts": {"test": "jest"}
    }

    (project_dir / "package.json").write_text(json.dumps(package_json))

    src_dir = project_dir / "src"
    src_dir.mkdir()
    (src_dir / "index.js").write_text("import React from 'react';")

    return str(project_dir)

def test_parse_package_json(temp_project):
    analyzer = DependencyAnalyzer(temp_project)
    deps = analyzer.parse_package_json()
    assert "react" in deps
    assert "jest" in deps

def test_find_unused_dependencies(temp_project):
    analyzer = DependencyAnalyzer(temp_project)
    unused = analyzer.find_unused_dependencies()
    # react is used in index.js
    # jest is used in scripts
    assert "react" not in unused
    assert "jest" not in unused

    # Add an unused dependency
    package_json_path = os.path.join(temp_project, "package.json")
    with open(package_json_path, "r") as f:
        data = json.load(f)
    data["dependencies"]["unused-lib"] = "1.0.0"
    with open(package_json_path, "w") as f:
        json.dump(data, f)

    unused = analyzer.find_unused_dependencies()
    assert "unused-lib" in unused

@pytest.mark.asyncio
async def test_analyze_bundle_size():
    analyzer = DependencyAnalyzer(".")
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"size": 1024, "gzip": 512}
        mock_get.return_value = mock_response

        result = await analyzer.analyze_bundle_size("react", "16.8.0")
        assert result["size"] == 1024

def test_check_duplicates(temp_project):
    analyzer = DependencyAnalyzer(temp_project)
    # create package-lock.json with duplicates
    lock_data = {
        "dependencies": {
            "dep-a": {
                "version": "1.0.0",
                "dependencies": {
                    "dep-b": {"version": "2.0.0"}
                }
            },
            "dep-b": {"version": "1.0.0"}
        }
    }
    with open(os.path.join(temp_project, "package-lock.json"), "w") as f:
        json.dump(lock_data, f)

    duplicates = analyzer.check_duplicates()
    assert "dep-b" in duplicates
    assert "1.0.0" in duplicates["dep-b"]
    assert "2.0.0" in duplicates["dep-b"]
