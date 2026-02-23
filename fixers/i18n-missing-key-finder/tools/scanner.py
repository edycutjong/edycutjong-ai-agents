import os
import re
from typing import List, Set, Pattern
from pathlib import Path

class Scanner:
    """
    Scans source code files for i18n keys using regex patterns.
    """

    DEFAULT_PATTERNS = [
        r"t\(\s*['\"](.+?)['\"]\s*\)",              # t('key')
        r"i18n\.t\(\s*['\"](.+?)['\"]\s*\)",         # i18n.t('key')
        r"trans\(\s*['\"](.+?)['\"]\s*\)",           # trans('key')
        r"_\(\s*['\"](.+?)['\"]\s*\)",               # _('key') for gettext
        r"\{\{\s*['\"](.+?)['\"]\s*\|\s*t\s*\}\}", # {{ 'key' | t }} (Liquid/Jinja)
    ]

    DEFAULT_IGNORE_DIRS = {
        'node_modules', '.git', 'venv', '.venv', '__pycache__', 'dist', 'build', 'coverage'
    }

    DEFAULT_EXTENSIONS = {
        '.js', '.ts', '.jsx', '.tsx', '.py', '.html', '.liquid', '.jinja', '.vue'
    }

    def __init__(self, patterns: List[str] = None, ignore_dirs: Set[str] = None, extensions: Set[str] = None):
        self.patterns = [re.compile(p) for p in (patterns or self.DEFAULT_PATTERNS)]
        self.ignore_dirs = ignore_dirs or self.DEFAULT_IGNORE_DIRS
        self.extensions = extensions or self.DEFAULT_EXTENSIONS

    def scan_file(self, filepath: str) -> Set[str]:
        """Scans a single file for keys."""
        keys = set()
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for pattern in self.patterns:
                    matches = pattern.findall(content)
                    keys.update(matches)
        except Exception as e:
            print(f"Error scanning file {filepath}: {e}")
        return keys

    def scan_directory(self, directory: str) -> Set[str]:
        """Recursively scans a directory for keys."""
        found_keys = set()
        for root, dirs, files in os.walk(directory):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            for file in files:
                if any(file.endswith(ext) for ext in self.extensions):
                    filepath = os.path.join(root, file)
                    found_keys.update(self.scan_file(filepath))
        return found_keys
