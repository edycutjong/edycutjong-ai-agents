import git
from pathlib import Path
from typing import Optional
import os

def get_repo(path: str = ".") -> git.Repo:
    try:
        return git.Repo(path, search_parent_directories=True)
    except git.InvalidGitRepositoryError:
        raise ValueError(f"No git repository found at {path}")

def get_current_branch(repo: git.Repo) -> str:
    try:
        return repo.active_branch.name
    except TypeError:
        # Happens if in detached HEAD
        return "HEAD"

def get_file_content_from_branch(repo: git.Repo, branch: str, file_path: str) -> Optional[str]:
    """
    Retrieves the content of a file from a specific branch.
    The file_path should be relative to the repository root or absolute.
    """
    try:
        commit = repo.commit(branch)

        # Resolve file path relative to repo root
        repo_root = Path(repo.working_dir).resolve()
        abs_file_path = Path(file_path).resolve()

        try:
            rel_path = abs_file_path.relative_to(repo_root)
        except ValueError:
            # If it's not relative to repo root, maybe user passed a relative path from CWD
            # Let's try to see if it works as is relative to repo root
            # Or if it's outside repo, we can't fetch it from git
            rel_path = Path(file_path)

        # Convert to string for gitpython
        target_path_str = str(rel_path).replace('\\', '/') # Ensure forward slashes for git

        # Access the file blob from the tree
        # This might fail if the file doesn't exist in that branch
        try:
            blob = commit.tree / target_path_str
            return blob.data_stream.read().decode('utf-8')
        except KeyError:
            print(f"File {target_path_str} not found in branch {branch}")
            return None

    except Exception as e:
        print(f"Error reading file from branch {branch}: {e}")
        return None
