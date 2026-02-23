import git
from typing import List, Dict, Optional
import datetime

def get_commits(repo_path: str, from_ref: Optional[str] = None, to_ref: str = "HEAD") -> List[Dict]:
    """
    Fetches commits from a git repository between two references.
    """
    try:
        repo = git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        raise ValueError(f"Invalid git repository at {repo_path}")

    # Build the revision range
    if from_ref:
        rev_range = f"{from_ref}..{to_ref}"
    else:
        rev_range = to_ref

    commits = []
    try:
        for commit in repo.iter_commits(rev_range):
            commits.append({
                "hash": commit.hexsha,
                "author": commit.author.name,
                "date": datetime.datetime.fromtimestamp(commit.committed_date).isoformat(),
                "message": commit.message.strip(),
                "files_changed": list(commit.stats.files.keys())
            })
    except git.exc.GitCommandError as e:
        raise ValueError(f"Error fetching commits: {e}")

    return commits

def format_commits_for_agent(commits: List[Dict]) -> str:
    """
    Formats the list of commits into a string for the agent.
    """
    formatted = ""
    for commit in commits:
        formatted += f"Hash: {commit['hash'][:7]}\n"
        formatted += f"Author: {commit['author']}\n"
        formatted += f"Date: {commit['date']}\n"
        formatted += f"Message: {commit['message']}\n"
        formatted += f"Files: {', '.join(commit['files_changed'])}\n"
        formatted += "-" * 20 + "\n"
    return formatted
