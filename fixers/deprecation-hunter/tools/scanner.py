import os
from pathlib import Path
from typing import List, Dict, Set
import re

def scan_directory(path: str) -> List[str]:
    """
    Recursively scans a directory for Python files.

    Args:
        path (str): The root path to scan.

    Returns:
        List[str]: A list of file paths to Python files.
    """
    python_files = []
    path_obj = Path(path)

    if not path_obj.exists():
        raise FileNotFoundError(f"The path {path} does not exist.")

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return python_files

def get_dependencies(path: str) -> Dict[str, str]:
    """
    Parses dependency files (requirements.txt, pyproject.toml) to find installed libraries.

    Args:
        path (str): The root path of the project.

    Returns:
        Dict[str, str]: A dictionary of package names and their versions (if specified).
    """
    dependencies = {}
    path_obj = Path(path)

    # Check requirements.txt
    req_file = path_obj / "requirements.txt"
    if req_file.exists():
        with open(req_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    # Basic parsing for requirements.txt
                    # Handles: package, package==version, package>=version, etc.
                    match = re.match(r"^([a-zA-Z0-9_\-]+)", line)
                    if match:
                        pkg_name = match.group(1).lower()
                        dependencies[pkg_name] = line # Store full line as version info for now

    # Check pyproject.toml (simple parsing)
    # Note: A full toml parser would be better, but for now we do simple string matching
    # or rely on regex if `tomllib` isn't available (it is in 3.11+).
    pyproject_file = path_obj / "pyproject.toml"
    if pyproject_file.exists():
        try:
            import tomllib
            with open(pyproject_file, "rb") as f:
                data = tomllib.load(f)

            # Poetry
            if "tool" in data and "poetry" in data["tool"] and "dependencies" in data["tool"]["poetry"]:
                for pkg, ver in data["tool"]["poetry"]["dependencies"].items():
                    dependencies[pkg.lower()] = str(ver)

            # Project (PEP 621)
            if "project" in data and "dependencies" in data["project"]:
                for dep in data["project"]["dependencies"]:
                    match = re.match(r"^([a-zA-Z0-9_\-]+)", dep)
                    if match:
                        dependencies[match.group(1).lower()] = dep

        except ImportError:
            # Fallback if tomllib is not available (should be in 3.11+)
            pass
        except Exception as e:
            print(f"Error parsing pyproject.toml: {e}")

    return dependencies
