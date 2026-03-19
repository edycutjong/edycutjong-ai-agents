from typing import List, Dict, Any
import os

def get_changed_files(repo_path: str, commit_sha: str = "HEAD") -> List[str]:
    """
    Returns a list of file paths changed in the given commit.
    Uses generic git command wrapper or just returns mocked for simple logic if gitpython isn't fully set up,
    but we will use gitpython.
    """
    try:
        from git import Repo
        repo = Repo(repo_path)
        commit = repo.commit(commit_sha)
        
        # If it has parents, diff against first parent. Otherwise it's the first commit.
        if commit.parents:
            parent = commit.parents[0]
            diffs = parent.diff(commit)
            files = []
            for d in diffs:
                if d.a_path:
                    files.append(d.a_path)
                elif d.b_path:
                    files.append(d.b_path)
            return list(set(files))
        else:
            return list(commit.stats.files.keys())
    except Exception:
        return []

def get_author_email(repo_path: str, commit_sha: str = "HEAD") -> str:
    try:
        from git import Repo
        repo = Repo(repo_path)
        commit = repo.commit(commit_sha)
        return commit.author.email
    except Exception:
        return ""
