import os
import shutil
import tempfile
import sys
import pytest

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.scanner import FileScanner
from agent.code_reader import CodeReader

@pytest.fixture
def temp_project():
    temp_dir = tempfile.mkdtemp()

    # Create structure
    os.makedirs(os.path.join(temp_dir, "src"))
    os.makedirs(os.path.join(temp_dir, "node_modules"))
    os.makedirs(os.path.join(temp_dir, ".git"))

    with open(os.path.join(temp_dir, "src", "main.py"), "w") as f:
        f.write("print('hello')")

    with open(os.path.join(temp_dir, "node_modules", "lib.js"), "w") as f:
        f.write("module.exports = {}")

    with open(os.path.join(temp_dir, ".gitignore"), "w") as f:
        f.write("node_modules/\n*.log")

    with open(os.path.join(temp_dir, "error.log"), "w") as f:
        f.write("error")

    yield temp_dir
    shutil.rmtree(temp_dir)

def test_scanner_ignores(temp_project):
    scanner = FileScanner(temp_project)
    # Re-initialize scanner to load gitignore correctly
    # But wait, scanner loads gitignore in __init__. So if I create .gitignore after creating scanner, it won't work.
    # The fixture creates files before yielding, so it should be fine.

    files = list(scanner.scan())

    rel_files = [os.path.relpath(f, temp_project) for f in files]

    # Debug
    print(f"Scanned files: {rel_files}")

    assert "src/main.py" in rel_files
    # Check if node_modules is ignored. The scanner should not yield files inside node_modules
    assert not any("node_modules" in f for f in rel_files)
    assert "error.log" not in rel_files
    # .git should be ignored
    assert not any(".git" in f for f in rel_files)

def test_scanner_extensions(temp_project):
    scanner = FileScanner(temp_project)
    py_files = scanner.get_source_files([".py"])
    rel_files = [os.path.relpath(f, temp_project) for f in py_files]

    assert "src/main.py" in rel_files
    assert len(rel_files) == 1

def test_code_reader(temp_project):
    file_path = os.path.join(temp_project, "src", "main.py")
    content = CodeReader.read_file(file_path)
    assert content == "print('hello')"

def test_code_reader_binary(temp_project):
    file_path = os.path.join(temp_project, "binary.bin")
    with open(file_path, "wb") as f:
        f.write(b'\x80\x81\x82') # Invalid utf-8

    content = CodeReader.read_file(file_path)
    assert content == ""

def test_code_reader_error(temp_project):
    # Non-existent file
    content = CodeReader.read_file("non_existent_file.txt")
    assert content == ""
