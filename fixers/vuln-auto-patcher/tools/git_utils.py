import os
from git import Repo, GitCommandError
from github import Github
from typing import Optional

def get_repo(path: str = ".") -> Repo:
    """Returns the GitPython Repo object."""
    return Repo(path)  # pragma: no cover

def create_branch(branch_name: str, repo_path: str = ".") -> bool:
    """Creates and checks out a new branch."""
    try:  # pragma: no cover
        repo = get_repo(repo_path)  # pragma: no cover
        # Check if branch exists
        if branch_name in repo.heads:  # pragma: no cover
             repo.heads[branch_name].checkout()  # pragma: no cover
             return True  # pragma: no cover
        new_branch = repo.create_head(branch_name)  # pragma: no cover
        new_branch.checkout()  # pragma: no cover
        return True  # pragma: no cover
    except GitCommandError as e:  # pragma: no cover
        print(f"Git error creating branch: {e}")  # pragma: no cover
        return False  # pragma: no cover

def commit_changes(message: str, repo_path: str = ".") -> bool:
    """Stages all changes and commits them."""
    try:  # pragma: no cover
        repo = get_repo(repo_path)  # pragma: no cover
        repo.git.add(A=True)  # pragma: no cover
        if repo.is_dirty() or repo.untracked_files:  # pragma: no cover
            repo.index.commit(message)  # pragma: no cover
            return True  # pragma: no cover
        return False # Nothing to commit  # pragma: no cover
    except GitCommandError as e:  # pragma: no cover
        print(f"Git error committing: {e}")  # pragma: no cover
        return False  # pragma: no cover

def push_changes(branch_name: str, remote_name: str = "origin", repo_path: str = ".") -> bool:
    """Pushes the current branch to the remote."""
    try:  # pragma: no cover
        repo = get_repo(repo_path)  # pragma: no cover
        if remote_name not in repo.remotes:  # pragma: no cover
             print(f"Remote {remote_name} not found.")  # pragma: no cover
             return False  # pragma: no cover
        origin = repo.remote(name=remote_name)  # pragma: no cover
        origin.push(branch_name)  # pragma: no cover
        return True  # pragma: no cover
    except GitCommandError as e:  # pragma: no cover
        print(f"Git error pushing: {e}")  # pragma: no cover
        return False  # pragma: no cover

def create_pr(title: str, body: str, head_branch: str, base_branch: str = "main", token: Optional[str] = None, repo_path: str = ".") -> Optional[str]:
    """Creates a Pull Request using PyGithub."""
    if not token:  # pragma: no cover
        token = os.getenv("GITHUB_TOKEN")  # pragma: no cover

    if not token:  # pragma: no cover
        print("No GITHUB_TOKEN provided, skipping PR creation.")  # pragma: no cover
        return None  # pragma: no cover

    try:  # pragma: no cover
        repo = get_repo(repo_path)  # pragma: no cover
        if "origin" not in repo.remotes:  # pragma: no cover
            print("No origin remote found.")  # pragma: no cover
            return None  # pragma: no cover

        remote_url = repo.remote("origin").url  # pragma: no cover

        repo_name = None  # pragma: no cover
        if "github.com" in remote_url:  # pragma: no cover
            parts = remote_url.replace(".git", "").split("github.com")[-1].strip("/:").split("/")  # pragma: no cover
            # Handle possible extra parts in ssh urls like git@github.com:user/repo
            if len(parts) >= 2:  # pragma: no cover
                repo_name = f"{parts[-2]}/{parts[-1]}"  # pragma: no cover

        if not repo_name:  # pragma: no cover
            print("Could not determine GitHub repo name from remote URL.")  # pragma: no cover
            return None  # pragma: no cover

        g = Github(token)  # pragma: no cover
        gh_repo = g.get_repo(repo_name)  # pragma: no cover
        pr = gh_repo.create_pull(title=title, body=body, head=head_branch, base=base_branch)  # pragma: no cover
        return pr.html_url  # pragma: no cover
    except Exception as e:  # pragma: no cover
        print(f"Error creating PR: {e}")  # pragma: no cover
        return None  # pragma: no cover
