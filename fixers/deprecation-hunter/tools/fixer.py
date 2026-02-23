import os
from typing import List
from .analyzer import DeprecationFinding

class DeprecationFixer:
    def fix_file(self, finding: DeprecationFinding) -> bool:
        """
        Applies a single fix to a file.
        Returns True if successful, False otherwise.
        """
        try:
            with open(finding.filepath, "r") as f:
                lines = f.readlines()

            # Line numbers are 1-indexed
            idx = finding.line_number - 1

            if idx < 0 or idx >= len(lines):
                print(f"Invalid line number {finding.line_number} for file {finding.filepath}")
                return False

            original_line = lines[idx]

            # Simple check: does the line contain the deprecated code?
            # The 'code' in finding might be just the function call "datetime.utcnow()"
            # The line might be "foo = datetime.utcnow()"
            # The suggestion might be "datetime.now(timezone.utc)"

            if finding.code in original_line and finding.suggestion:
                new_line = original_line.replace(finding.code, finding.suggestion)
                lines[idx] = new_line

                with open(finding.filepath, "w") as f:
                    f.writelines(lines)
                return True
            else:
                print(f"Could not find exact match for '{finding.code}' in line {finding.line_number}: {original_line.strip()}")
                return False

        except Exception as e:
            print(f"Error fixing file {finding.filepath}: {e}")
            return False

    def apply_fixes(self, findings: List[DeprecationFinding]) -> int:
        """
        Applies multiple fixes. Sorts them in reverse line order to avoid offsetting.
        Note: This is risky if multiple fixes are on the same line or overlapping.
        Ideally we should group by file and apply carefully.
        """
        # Group by file
        files_map = {}
        for f in findings:
            if f.filepath not in files_map:
                files_map[f.filepath] = []
            files_map[f.filepath].append(f)

        success_count = 0

        for filepath, file_findings in files_map.items():
            # Sort by line number descending
            file_findings.sort(key=lambda x: x.line_number, reverse=True)

            for finding in file_findings:
                if self.fix_file(finding):
                    success_count += 1

        return success_count
