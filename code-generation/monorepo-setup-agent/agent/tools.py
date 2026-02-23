import os
import subprocess
from pathlib import Path
from typing import Optional

def make_directory(path: str):
    """Creates a directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)

def write_file_content(path: str, content: str):
    """Writes content to a file, ensuring the directory exists."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)

def run_command(command: str, cwd: Optional[str] = None) -> tuple[int, str, str]:
    """Runs a shell command."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)
