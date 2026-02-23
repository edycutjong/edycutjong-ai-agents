import subprocess
from typing import Dict, Any

def run_tests(project_path: str = ".") -> Dict[str, Any]:
    """Runs the project's test suite."""
    try:
        # npm test typically exits with non-zero on failure
        result = subprocess.run(
            ["npm", "test"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
