import pytest
from unittest.mock import MagicMock, patch, mock_open
import os
from tools.doc_manager import DocManager

def test_scan_docs():
    with patch('os.walk') as mock_walk:
        mock_walk.return_value = [
            ('.', [], ['README.md', 'agent.py']),
            ('./docs', [], ['api.md'])
        ]
        manager = DocManager()
        docs = manager.scan_docs()
        assert len(docs) == 2
        assert './README.md' in docs
        assert './docs/api.md' in docs

def test_find_related_docs():
    with patch.object(DocManager, 'scan_docs', return_value=['docs/utils.md', 'docs/api.md']):
        manager = DocManager()
        related = manager.find_related_docs('src/utils.py')
        assert 'docs/utils.md' in related
        assert 'docs/api.md' not in related

def test_check_links_local():
    with patch('builtins.open', mock_open(read_data="[link](existing.md)")):
        with patch('os.path.exists', return_value=True):
            manager = DocManager()
            broken = manager.check_links('doc.md')
            assert len(broken) == 0

    with patch('builtins.open', mock_open(read_data="[link](missing.md)")):
        with patch('os.path.exists', return_value=False):
            manager = DocManager()
            broken = manager.check_links('doc.md')
            assert len(broken) == 1
            assert "missing.md" in broken[0]

def test_check_links_anchor():
    # Test link with anchor
    with patch('builtins.open', mock_open(read_data="[link](existing.md#section)")):
        with patch('os.path.exists') as mock_exists:
             # It should check existing.md
             mock_exists.return_value = True
             manager = DocManager()
             broken = manager.check_links('doc.md')
             assert len(broken) == 0
             # We can't easily assert split behavior with just return value check unless we inspect calls
             # mock_exists should have been called with absolute path or relative path depending on impl.
             # In impl: os.path.join(doc_dir, link) then split.
             # doc_dir is "" for 'doc.md'
             mock_exists.assert_called_with('existing.md')

def test_verify_code_examples():
    code_good = "```python\nprint('hello')\n```"
    code_bad = "```python\nprint('hello'\n```" # Missing closing paren

    with patch('builtins.open', mock_open(read_data=code_good)):
        manager = DocManager()
        errors = manager.verify_code_examples('doc.md')
        assert len(errors) == 0

    with patch('builtins.open', mock_open(read_data=code_bad)):
        manager = DocManager()
        errors = manager.verify_code_examples('doc.md')
        assert len(errors) == 1
        assert "SyntaxError" in errors[0]
