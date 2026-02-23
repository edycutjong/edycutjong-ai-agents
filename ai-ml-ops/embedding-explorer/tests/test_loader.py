import pytest
import sys
import os

# Add parent directory to path to import agent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.loader import DataLoader

@pytest.fixture
def sample_text_file(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("Hello World!", encoding="utf-8")
    return p

def test_load_text_file(sample_text_file):
    content = DataLoader.load_text_file(str(sample_text_file))
    assert content == "Hello World!"

def test_load_file_dispatch(sample_text_file):
    content = DataLoader.load_file(str(sample_text_file))
    assert content == "Hello World!"

def test_load_unsupported_file():
    with pytest.raises(ValueError):
        DataLoader.load_file("test.xyz")

def test_split_text():
    text = "A" * 2000
    chunks = DataLoader.split_text(text, chunk_size=1000, chunk_overlap=0)
    assert len(chunks) == 2
    assert len(chunks[0]) == 1000
