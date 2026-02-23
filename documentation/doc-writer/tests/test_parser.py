import os
import tempfile
import sys
from doc_writer.parser import CodeParser

# Add the project root to sys.path to ensure imports work when running pytest from outside
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_find_missing_docstrings():
    code = """
def my_function(a, b):
    return a + b

class MyClass:
    def method(self):
        pass

def documented_function():
    "This is a docstring"
    pass
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name
        tmp.close() # Close file handle so parser can read it

    try:
        parser = CodeParser()
        targets = parser.find_missing_docstrings(tmp_path)

        # Check targets
        # Note: CodeParser finds methods inside classes too if they are missing docstrings.
        # In this case:
        # 1. my_function (missing)
        # 2. MyClass (missing)
        # 3. method (missing) inside MyClass

        # Let's see what the parser returns. It uses ast.walk which traverses all nodes.
        # So it should find 'method' too.

        names = [t.name for t in targets]
        assert "my_function" in names
        assert "MyClass" in names
        assert "method" in names
        assert "documented_function" not in names

        assert len(targets) == 3

    finally:
        os.remove(tmp_path)
