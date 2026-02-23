import subprocess
from typing import List

class StyleFixer:
    def __init__(self, ignore_patterns: List[str] = None):
        self.ignore_patterns = ignore_patterns or []

    def fix_file(self, filepath: str) -> bool:
        """Applies fixes to a single file using autopep8."""
        if self._should_ignore(filepath):
            return False

        try:
            result = subprocess.run(
                ["autopep8", "--in-place", "--aggressive", "--aggressive", filepath],
                capture_output=True,
                check=False
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error fixing file {filepath}: {e}")
            return False

    def _should_ignore(self, filepath: str) -> bool:
        for pattern in self.ignore_patterns:
            if pattern in filepath:
                return True
        return False
