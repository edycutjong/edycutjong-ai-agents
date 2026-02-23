import subprocess
import os
import re
from typing import Dict, Any

class TestRunner:
    def __init__(self, headless: bool = True):
        self.headless = headless

    def run_tests(self, test_file_path: str) -> Dict[str, Any]:
        """
        Runs the specified test file using pytest and returns the result.
        """
        if not os.path.exists(test_file_path):
            return {
                "success": False,
                "output": f"Test file not found: {test_file_path}",
                "passed": 0,
                "failed": 0,
                "total": 0
            }

        # Construct the command
        # We assume pytest is installed in the environment
        cmd = ["pytest", test_file_path, "--verbose"]

        if not self.headless:
            cmd.append("--headed")

        # If running in a specific environment, we might need to activate it,
        # but subprocess inherits the current environment by default.

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False  # Don't raise exception on test failure (exit code 1)
            )

            output = result.stdout + "\n" + result.stderr
            success = result.returncode == 0

            # Parse pytest summary output
            passed = 0
            failed = 0

            # Look for summary line: "1 failed, 1 passed in 0.12s"
            summary_match = re.search(r'(\d+)\s+passed', output)
            if summary_match:
                passed = int(summary_match.group(1))

            summary_match_failed = re.search(r'(\d+)\s+failed', output)
            if summary_match_failed:
                failed = int(summary_match_failed.group(1))

            total = passed + failed

            return {
                "success": success,
                "output": output,
                "passed": passed,
                "failed": failed,
                "total": total
            }

        except Exception as e:
            return {
                "success": False,
                "output": str(e),
                "passed": 0,
                "failed": 0,
                "total": 0
            }
