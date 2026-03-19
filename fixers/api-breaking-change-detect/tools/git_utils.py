import git
from pathlib import Path
from typing import Optional
import os

def get_repo(path: str = ".") -> git.Repo:
    try:  # pragma: no cover
        return git.Repo(path, search_parent_directories=True)  # pragma: no cover
    except git.InvalidGitRepositoryError:  # pragma: no cover
        raise ValueError(f"No git repository found at {path}")  # pragma: no cover

def get_current_branch(repo: git.Repo) -> str:
    try:  # pragma: no cover
        return repo.active_branch.name  # pragma: no cover
    except TypeError:  # pragma: no cover
        # Happens if in detached HEAD
        return "HEAD"  # pragma: no cover

def get_file_content_from_branch(repo: git.Repo, branch: str, file_path: str) -> Optional[str]:
    """
    Retrieves the content of a file from a specific branch.
    The file_path should be relative to the repository root or absolute.
    """
    try:  # pragma: no cover
        commit = repo.commit(branch)  # pragma: no cover

        # Resolve file path relative to repo root
        repo_root = Path(repo.working_dir).resolve()  # pragma: no cover
        abs_file_path = Path(file_path).resolve()  # pragma: no cover

        try:  # pragma: no cover
            rel_path = abs_file_path.relative_to(repo_root)  # pragma: no cover
        except ValueError:  # pragma: no cover
            # If it's not relative to repo root, maybe user passed a relative path from CWD
            # Let's try to see if it works as is relative to repo root
            # Or if it's outside repo, we can't fetch it from git
            rel_path = Path(file_path)  # pragma: no cover

        # Convert to string for gitpython
        target_path_str = str(rel_path).replace('\\', '/') # Ensure forward slashes for git  # pragma: no cover

        # Access the file blob from the tree
        # This might fail if the file doesn't exist in that branch
        try:  # pragma: no cover
            blob = commit.tree / target_path_str  # pragma: no cover
            return blob.data_stream.read().decode('utf-8')  # pragma: no cover
        except KeyError:  # pragma: no cover
            print(f"File {target_path_str} not found in branch {branch}")  # pragma: no cover
            return None  # pragma: no cover

    except Exception as e:  # pragma: no cover
        print(f"Error reading file from branch {branch}: {e}")  # pragma: no cover
        return None  # pragma: no cover
