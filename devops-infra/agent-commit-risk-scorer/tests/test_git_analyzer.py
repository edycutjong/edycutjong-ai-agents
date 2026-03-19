import pytest
import sys
from lib.git_analyzer import get_changed_files, get_author_email

def test_get_changed_files_success(mocker):
    class MockDiff:
        def __init__(self, a, b):
            self.a_path = a
            self.b_path = b

    class MockCommit:
        def __init__(self, parents=True):
            if parents:
                self.parents = [type('obj', (object,), {'diff': lambda self, commit: [MockDiff('src/main.py', None), MockDiff(None, 'README.md')]})()]
            else:
                self.parents = []
                self.stats = type('Stats', (), {'files': {'src/main.py': 10, 'README.md': 2}})

    class MockRepo:
        def __init__(self, *args, **kwargs):
            pass
        def commit(self, sha):
            return MockCommit(parents=True)
            
    mocker.patch('git.Repo', MockRepo)
    
    files = get_changed_files('.', 'HEAD')
    assert sorted(files) == sorted(['src/main.py', 'README.md'])

def test_get_changed_files_no_parents(mocker):
    class MockCommit:
        def __init__(self):
            self.parents = []
            self.stats = type('Stats', (), {'files': {'src/main.py': 10}})

    class MockRepo:
        def __init__(self, *args, **kwargs):
            pass
        def commit(self, sha):
            return MockCommit()
            
    mocker.patch('git.Repo', MockRepo)
    
    files = get_changed_files('.', 'HEAD')
    assert files == ['src/main.py']

def test_get_changed_files_error(mocker):
    mocker.patch('git.Repo', side_effect=Exception("Git error"))
    files = get_changed_files('.', 'HEAD')
    assert files == []

def test_get_author_email_success(mocker):
    class MockCommit:
        def __init__(self):
            self.author = type('Author', (), {'email': 'test@example.com'})()

    class MockRepo:
        def __init__(self, *args, **kwargs):
            pass
        def commit(self, sha):
            return MockCommit()
            
    mocker.patch('git.Repo', MockRepo)
    
    email = get_author_email('.', 'HEAD')
    assert email == "test@example.com"

def test_get_author_email_error(mocker):
    mocker.patch('git.Repo', side_effect=Exception("Git error"))
    email = get_author_email('.', 'HEAD')
    assert email == ""
