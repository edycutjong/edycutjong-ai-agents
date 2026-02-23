import os
import shutil
import pytest
from tools.visualizer import Visualizer

@pytest.fixture
def temp_output(tmp_path):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    yield output_dir
    # cleanup handled by tmp_path

def test_generate_report(temp_output):
    visualizer = Visualizer(str(temp_output))
    dependency_sizes = [{"name": "react", "size": 1024, "gzip": 512}]
    unused_deps = ["lodash"]
    duplicates = {"lodash": ["1.0.0", "2.0.0"]}
    suggestions = ["Suggestion 1"]

    report_path = visualizer.generate_report(dependency_sizes, unused_deps, duplicates, suggestions)
    assert os.path.exists(report_path)
    with open(report_path, "r") as f:
        content = f.read()
        assert "react" in content
        assert "lodash" in content
        assert "Suggestion 1" in content

def test_generate_treemap(temp_output):
    visualizer = Visualizer(str(temp_output))
    dependency_sizes = [{"name": "react", "size": 1024}]
    treemap_html = visualizer.generate_treemap(dependency_sizes)
    assert "react" in treemap_html
    assert "div" in treemap_html
