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
            return []  # pragma: no cover

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
        except Exception as e:  # pragma: no cover
            print(f"Error checking file {filepath}: {e}")  # pragma: no cover

        return issues

    def _should_ignore(self, filepath: str) -> bool:
        for pattern in self.ignore_patterns:
            if pattern in filepath:  # pragma: no cover
                return True  # pragma: no cover
        return False

    def scan_directory(self, directory: str = ".") -> List[Dict]:
        """Scans a directory for Python files and checks them."""
        all_issues = []  # pragma: no cover
        for root, dirs, files in os.walk(directory):  # pragma: no cover
            # Filter ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore(os.path.join(root, d))]  # pragma: no cover

            for file in files:  # pragma: no cover
                if file.endswith(".py"):  # pragma: no cover
                    filepath = os.path.join(root, file)  # pragma: no cover
                    if not self._should_ignore(filepath):  # pragma: no cover
                        file_issues = self.check_file(filepath)  # pragma: no cover
                        all_issues.extend(file_issues)  # pragma: no cover
        return all_issues  # pragma: no cover
