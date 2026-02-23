import re
from collections import Counter
from typing import List, Tuple

class LogAnalyzer:
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        self.logs: List[str] = []
        self.patterns: Counter = Counter()

    def read_logs(self):
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                self.logs = f.readlines()
        except FileNotFoundError:
            print(f"Error: File {self.log_file_path} not found.")
            self.logs = []
        except Exception as e:
            print(f"Error reading file: {e}")
            self.logs = []

    def analyze(self) -> List[Tuple[str, int]]:
        """
        Analyzes logs and returns a list of (pattern, count) tuples, sorted by count descending.
        """
        self.patterns.clear()
        for line in self.logs:
            if not line.strip():
                continue
            normalized_line = self._normalize_line(line.strip())
            self.patterns[normalized_line] += 1

        return self.patterns.most_common()

    def _normalize_line(self, line: str) -> str:
        # Replace timestamps (ISO 8601-ish)
        line = re.sub(r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})?', '<TIMESTAMP>', line)
        # Replace common date formats like 27/Oct/2023
        line = re.sub(r'\d{1,2}/[A-Za-z]{3}/\d{4}', '<DATE>', line)

        # Replace UUIDs
        line = re.sub(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', '<UUID>', line)

        # Replace IPv4
        line = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '<IP>', line)

        # Replace numbers (integer and float)
        line = re.sub(r'\b\d+\.?\d*\b', '<NUM>', line)

        # Replace hex
        line = re.sub(r'0x[0-9a-fA-F]+', '<HEX>', line)

        # Replace quoted strings (sometimes specific IDs are in quotes) - this is aggressive so maybe skip
        # line = re.sub(r'"[^"]*"', '"<STR>"', line)

        return line
