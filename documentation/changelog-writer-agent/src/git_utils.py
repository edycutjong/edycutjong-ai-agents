"""Git utilities for changelog generation."""
import git
from datetime import datetime


def get_commits(repo_path: str, from_ref: str = "HEAD~10", to_ref: str = "HEAD") -> list[dict]:
    """Get commits from a git repository between two refs."""
    repo = git.Repo(repo_path)
    commits = []
    for commit in repo.iter_commits(f"{from_ref}..{to_ref}"):
        commits.append({
            "hash": commit.hexsha,
            "short_hash": commit.hexsha[:7],
            "author": commit.author.name,
            "date": datetime.fromtimestamp(commit.committed_date).isoformat(),
            "message": commit.message.strip(),
            "files_changed": list(commit.stats.files.keys()),
        })
    return commits


def format_commits_for_agent(commits: list[dict]) -> str:
    """Format commits into a string for the AI agent."""
    lines = []
    for c in commits:
        lines.append(f"- [{c['short_hash']}] {c['message']} (by {c['author']}, {c['date']}, files: {', '.join(c['files_changed'][:5])})")
    return "\n".join(lines)
