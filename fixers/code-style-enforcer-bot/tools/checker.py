import subprocess
import os
import re
from typing import List, Dict

class StyleChecker:
    def __init__(self, ignore_patterns: List[str] = None):
        self.ignore_patterns = ignore_patterns or []

    def check_file(self, filepath: str) -> List[Dict]:
        """Runs flake8 on a file and returns a list of issues."""
        if self._should_ignore(filepath):
            return []

        issues = []
        try:
            # Run flake8 and capture output
            result = subprocess.run(
                ["flake8", "--format=%(path)s:%(row)d:%(col)d: %(code)s %(text)s", filepath],
                capture_output=True,
                text=True,
                check=False
            )

            if result.stdout:
                for line in result.stdout.splitlines():
                    match = re.match(r"(?P<path>.*):(?P<row>\d+):(?P<col>\d+): (?P<code>\w+) (?P<text>.*)", line)
                    if match:
                        issues.append(match.groupdict())
        except Exception as e:
            print(f"Error checking file {filepath}: {e}")

        return issues

    def _should_ignore(self, filepath: str) -> bool:
        for pattern in self.ignore_patterns:
            if pattern in filepath:
                return True
        return False

    def scan_directory(self, directory: str = ".") -> List[Dict]:
        """Scans a directory for Python files and checks them."""
        all_issues = []
        for root, dirs, files in os.walk(directory):
            # Filter ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore(os.path.join(root, d))]

            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    if not self._should_ignore(filepath):
                        file_issues = self.check_file(filepath)
                        all_issues.extend(file_issues)
        return all_issues
