import subprocess
import shutil
import json
from typing import Optional

def get_installed_version(package_name: str, project_path: str = ".") -> Optional[str]:
    """Gets the currently installed version of a package."""
    try:
        # npm list returns non-zero if peer dep issues, so check=False
        result = subprocess.run(
            ["npm", "list", package_name, "--depth=0", "--json"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False
        )
        if not result.stdout.strip():
            return None

        data = json.loads(result.stdout)
        # Check dependencies
        if "dependencies" in data and package_name in data["dependencies"]:
            return data["dependencies"][package_name].get("version")
        # Check devDependencies if not found in dependencies?
        # Actually npm list includes both by default unless --prod/--dev specified.
        return None
    except Exception as e:
        print(f"Error getting version for {package_name}: {e}")
        return None

def update_package(package_name: str, version: str, project_path: str = ".") -> bool:
    """Updates a package to a specific version using npm install."""
    try:
        subprocess.run(
            ["npm", "install", f"{package_name}@{version}", "--save-exact"],
            cwd=project_path,
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def update_lockfile(project_path: str = ".") -> bool:
    """Updates the lockfile (package-lock.json)."""
    try:
        subprocess.run(
            ["npm", "install", "--package-lock-only"],
            cwd=project_path,
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError:
        return False
