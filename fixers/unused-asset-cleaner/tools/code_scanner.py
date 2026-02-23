import os
import re
from pathlib import Path
from typing import List, Set, Dict, Tuple
from collections import defaultdict

class CodeScanner:
    """
    Scans source code for references to assets.
    """

    # Extensions of files where we expect to find asset references
    SOURCE_EXTENSIONS = {
        '.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte',
        '.html', '.css', '.scss', '.sass', '.less',
        '.json', '.md', '.py', '.rb', '.php', '.java', '.c', '.cpp', '.h', '.go', '.rs',
        '.yml', '.yaml'
    }

    def __init__(self, root_dir: str, ignore_dirs: List[str] = None):
        self.root_dir = Path(root_dir)
        self.ignore_dirs = set(ignore_dirs) if ignore_dirs else {
            '.git', 'node_modules', 'dist', 'build', '__pycache__', 'venv', '.next', '.idea', '.vscode'
        }

    def _should_ignore(self, path: Path) -> bool:
        parts = path.parts
        for part in parts:
            if part in self.ignore_dirs:
                return True
        return False

    def _get_source_files(self) -> List[Path]:
        """
        Recursively finds all source code files.
        """
        source_files = []
        for root, dirs, files in os.walk(self.root_dir):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.SOURCE_EXTENSIONS:
                    source_files.append(file_path)
        return source_files

    def find_references(self, assets: List[Path]) -> Dict[Path, Set[Path]]:
        """
        Finds which assets are referenced in the code.
        Returns a dictionary mapping Asset Path -> Set of Source Files where it's used.
        """
        # Map filename -> List of Asset Paths with that filename
        asset_name_map = defaultdict(list)
        asset_stem_map = defaultdict(list)

        for asset in assets:
            asset_name_map[asset.name].append(asset)
            # Map stem for extensionless imports (e.g., 'logo' from 'logo.png')
            # But only if it's a typical asset extension that might be omitted or is a code file itself
            # We focus on images/media where extension might be omitted in bundlers or code
            if asset.suffix.lower() in {'.js', '.ts', '.jsx', '.tsx', '.vue', '.svelte', '.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp'}:
                asset_stem_map[asset.stem].append(asset)

        references = {asset: set() for asset in assets}

        source_files = self._get_source_files()

        # Regex to find string literals: matches 'string' or "string" handling escaped quotes
        string_pattern = re.compile(r"(['\"])(?:\\.|(?!\1).)*\1")

        for source_file in source_files:
            try:
                # Read file content
                with open(source_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # 1. Check for exact filenames (fast string search)
                for asset_name, asset_paths in asset_name_map.items():
                    if asset_name in content:
                        for asset_path in asset_paths:
                            references[asset_path].add(source_file)

                # 2. Check for stems (extensionless) inside quotes
                for match in string_pattern.finditer(content):
                    full_match = match.group(0)
                    string_content = full_match[1:-1] # strip quotes

                    parts = string_content.split('/')
                    filename_part = parts[-1]

                    if filename_part in asset_stem_map:
                         for asset_path in asset_stem_map[filename_part]:
                            references[asset_path].add(source_file)

            except Exception as e:
                # Ignore errors reading files
                pass

        return references

if __name__ == "__main__":
    pass
