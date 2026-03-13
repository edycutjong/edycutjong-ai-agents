import sys
import io
import contextlib
import requests
import ast
import builtins
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional, Set

def extract_text_from_url(url: str) -> str:
    """
    Fetches the content of a URL and extracts the main text.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator='\n')
        # Break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Drop blank lines
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

def is_safe_code(code: str) -> bool:
    """
    Checks if the Python code snippet is safe to execute via AST analysis.
    Disallows imports of dangerous modules, calls to dangerous functions,
    and access to dangerous attributes used for sandbox escapes.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False  # Syntax error is technically safe but not executable

    unsafe_modules = {'os', 'sys', 'subprocess', 'shutil', 'socket', 'requests', 'http', 'urllib', 'builtins', 'pickle'}
    unsafe_functions = {'open', 'eval', 'exec', 'compile', 'getattr', 'setattr', 'delattr', 'input', '__import__', 'globals', 'locals'}
    unsafe_attributes = {'__class__', '__bases__', '__subclasses__', '__mro__', '__globals__', '__builtins__', '__dict__', '__code__', '__closure__', '__doc__', '__name__', '__module__'}

    for node in ast.walk(tree):
        # Check imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] in unsafe_modules:
                    return False
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split('.')[0] in unsafe_modules:
                return False

        # Check function calls
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in unsafe_functions:
                    return False

        # Check attribute access (prevents sandbox escapes via reflection)
        if isinstance(node, ast.Attribute):
            if node.attr in unsafe_attributes:
                return False

    return True

def execute_python_snippet(code: str, timeout: int = 5) -> Dict[str, Any]:
    """
    Executes a Python code snippet and returns the stdout, stderr, and any exception.
    Warning: This uses exec() and is sandboxed only by static analysis and restricted globals.
    """
    # Create a buffer to capture stdout and stderr
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    result = {
        "stdout": "",
        "stderr": "",
        "error": None,
        "success": False
    }

    if not is_safe_code(code):
        result["error"] = "Code execution blocked: Safety check failed (dangerous imports/functions)."
        return result

    try:
        # Define safe builtins
        safe_builtins_names = {
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
            'callable', 'chr', 'classmethod', 'complex', 'dict', 'divmod',
            'enumerate', 'filter', 'float', 'format', 'frozenset', 'hash',
            'help', 'hex', 'id', 'int', 'isinstance', 'issubclass', 'iter',
            'len', 'list', 'map', 'max', 'memoryview', 'min', 'next',
            'oct', 'ord', 'pow', 'print', 'property', 'range',
            'repr', 'reversed', 'round', 'set', 'slice', 'sorted',
            'staticmethod', 'str', 'sum', 'super', 'tuple', 'vars', 'zip'
        }

        # Construct restricted __builtins__
        restricted_builtins = {
            name: getattr(builtins, name)
            for name in safe_builtins_names
            if hasattr(builtins, name)
        }

        # Add basic exceptions
        exceptions = [name for name in dir(builtins) if name.endswith('Error') or name.endswith('Exception')]
        for exc in exceptions:
            if hasattr(builtins, exc):
                restricted_builtins[exc] = getattr(builtins, exc)

        exec_globals = {"__builtins__": restricted_builtins}

        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            exec(code, exec_globals)

        result["success"] = True
    except Exception as e:
        result["error"] = str(e)

    result["stdout"] = stdout_buffer.getvalue()
    result["stderr"] = stderr_buffer.getvalue()

    return result

def extract_code_blocks(content: str, language: str = "python") -> list[str]:
    """
    Extracts code blocks for a specific language from markdown content.
    """
    import re
    # Match ```python ... ``` or just indented blocks if we want, but markdown fences are standard
    pattern = re.compile(f"```{language}(.*?)```", re.DOTALL | re.IGNORECASE)
    matches = pattern.findall(content)
    return [match.strip() for match in matches]
