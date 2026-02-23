import pytest
import sys
import os

# Append the project root to sys.path so we can import 'agent'
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from agent.schema_loader import SchemaLoader

def test_load_from_file(tmp_path):
    loader = SchemaLoader()
    d = tmp_path / "schema.sql"
    d.write_text("CREATE TABLE users (id INT PRIMARY KEY);")

    content = loader.load_from_file(str(d))
    assert "CREATE TABLE users" in content

def test_load_from_missing_file():
    loader = SchemaLoader()
    with pytest.raises(FileNotFoundError):
        loader.load_from_file("non_existent_file.sql")

def test_load_from_directory(tmp_path):
    loader = SchemaLoader()
    d1 = tmp_path / "1_users.sql"
    d1.write_text("CREATE TABLE users (id INT PRIMARY KEY);")
    d2 = tmp_path / "2_posts.sql"
    d2.write_text("CREATE TABLE posts (id INT PRIMARY KEY);")

    content = loader.load_from_directory(str(tmp_path))
    assert "CREATE TABLE users" in content
    assert "CREATE TABLE posts" in content

def test_load_from_missing_directory():
    loader = SchemaLoader()
    with pytest.raises(NotADirectoryError):
        loader.load_from_directory("non_existent_dir")
