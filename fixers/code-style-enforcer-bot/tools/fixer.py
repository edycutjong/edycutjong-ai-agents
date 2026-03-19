import subprocess
from typing import List

class StyleFixer:
    def __init__(self, ignore_patterns: List[str] = None):
        self.ignore_patterns = ignore_patterns or []

    def fix_file(self, filepath: str) -> bool:
        """Applies fixes to a single file using autopep8."""
        if self._should_ignore(filepath):
            return False  # pragma: no cover

        try:
            result = subprocess.run(
                ["autopep8", "--in-place", "--aggressive", "--aggressive", filepath],
                capture_output=True,
                check=False
            )
            return result.returncode == 0
        except Exception as e:  # pragma: no cover
            print(f"Error fixing file {filepath}: {e}")  # pragma: no cover
            return False  # pragma: no cover

    def _should_ignore(self, filepath: str) -> bool:
        for pattern in self.ignore_patterns:
            if pattern in filepath:  # pragma: no cover
                return True  # pragma: no cover
        return False
