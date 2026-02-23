import os
import tempfile
import sys
from doc_writer.modifier import insert_docstring

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_insert_docstring_trailing_comment():
    code = """
def foo(a, b): # This is a comment
    return a + b
"""
    docstring = "This is a docstring."
    expected_code = """
def foo(a, b): # This is a comment
    \"\"\"
    This is a docstring.
    \"\"\"
    return a + b
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name
        tmp.close()

    try:
        # foo starts on line 2
        success = insert_docstring(tmp_path, 2, docstring)
        assert success

        with open(tmp_path, 'r') as f:
            content = f.read()

        # Normalize line endings and whitespace for comparison
        # Or just check if docstring is inserted correctly

        lines = content.splitlines()
        # line 0 is empty
        # line 1 is def foo...
        # line 2 should be indented """
        assert '"""' in lines[2]
        assert 'This is a docstring.' in lines[3]
        assert '"""' in lines[4]
        assert 'return a + b' in lines[5]

    finally:
        os.remove(tmp_path)
