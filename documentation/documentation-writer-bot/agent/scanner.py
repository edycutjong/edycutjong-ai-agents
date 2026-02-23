import os
import pathspec
from typing import List, Generator

class FileScanner:
    def __init__(self, root_dir: str):
        self.root_dir = os.path.abspath(root_dir)
        self.gitignore = self._load_gitignore()

    def _load_gitignore(self) -> pathspec.PathSpec:
        gitignore_path = os.path.join(self.root_dir, ".gitignore")
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as f:
                spec = pathspec.PathSpec.from_lines("gitignore", f)
                return spec
        return pathspec.PathSpec.from_lines("gitignore", [])

    def scan(self) -> Generator[str, None, None]:
        for root, dirs, files in os.walk(self.root_dir):
            # Filter directories
            dirs[:] = [d for d in dirs if not self._is_ignored(os.path.join(root, d))]

            for file in files:
                file_path = os.path.join(root, file)
                if not self._is_ignored(file_path):
                    yield file_path

    def _is_ignored(self, path: str) -> bool:
        rel_path = os.path.relpath(path, self.root_dir)
        if rel_path.startswith(".git"): # Always ignore .git folder content
            return True
        return self.gitignore.match_file(rel_path)

    def get_source_files(self, extensions: List[str] = None) -> List[str]:
        files = list(self.scan())
        if extensions:
            return [f for f in files if any(f.endswith(ext) for ext in extensions)]
        return files
