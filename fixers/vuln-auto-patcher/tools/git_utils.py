import os
from git import Repo, GitCommandError
from github import Github
from typing import Optional

def get_repo(path: str = ".") -> Repo:
    """Returns the GitPython Repo object."""
    return Repo(path)

def create_branch(branch_name: str, repo_path: str = ".") -> bool:
    """Creates and checks out a new branch."""
    try:
        repo = get_repo(repo_path)
        # Check if branch exists
        if branch_name in repo.heads:
             repo.heads[branch_name].checkout()
             return True
        new_branch = repo.create_head(branch_name)
        new_branch.checkout()
        return True
    except GitCommandError as e:
        print(f"Git error creating branch: {e}")
        return False

def commit_changes(message: str, repo_path: str = ".") -> bool:
    """Stages all changes and commits them."""
    try:
        repo = get_repo(repo_path)
        repo.git.add(A=True)
        if repo.is_dirty() or repo.untracked_files:
            repo.index.commit(message)
            return True
        return False # Nothing to commit
    except GitCommandError as e:
        print(f"Git error committing: {e}")
        return False

def push_changes(branch_name: str, remote_name: str = "origin", repo_path: str = ".") -> bool:
    """Pushes the current branch to the remote."""
    try:
        repo = get_repo(repo_path)
        if remote_name not in repo.remotes:
             print(f"Remote {remote_name} not found.")
             return False
        origin = repo.remote(name=remote_name)
        origin.push(branch_name)
        return True
    except GitCommandError as e:
        print(f"Git error pushing: {e}")
        return False

def create_pr(title: str, body: str, head_branch: str, base_branch: str = "main", token: Optional[str] = None, repo_path: str = ".") -> Optional[str]:
    """Creates a Pull Request using PyGithub."""
    if not token:
        token = os.getenv("GITHUB_TOKEN")

    if not token:
        print("No GITHUB_TOKEN provided, skipping PR creation.")
        return None

    try:
        repo = get_repo(repo_path)
        if "origin" not in repo.remotes:
            print("No origin remote found.")
            return None

        remote_url = repo.remote("origin").url

        repo_name = None
        if "github.com" in remote_url:
            parts = remote_url.replace(".git", "").split("github.com")[-1].strip("/:").split("/")
            # Handle possible extra parts in ssh urls like git@github.com:user/repo
            if len(parts) >= 2:
                repo_name = f"{parts[-2]}/{parts[-1]}"

        if not repo_name:
            print("Could not determine GitHub repo name from remote URL.")
            return None

        g = Github(token)
        gh_repo = g.get_repo(repo_name)
        pr = gh_repo.create_pull(title=title, body=body, head=head_branch, base=base_branch)
        return pr.html_url
    except Exception as e:
        print(f"Error creating PR: {e}")
        return None
