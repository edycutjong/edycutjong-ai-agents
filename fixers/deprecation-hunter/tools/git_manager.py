import os
import git
from typing import Optional
from github import Github

class GitManager:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        try:
            self.repo = git.Repo(repo_path)
        except git.exc.InvalidGitRepositoryError:
            print(f"Not a git repository: {repo_path}")
            self.repo = None

    def create_branch(self, branch_name: str) -> bool:
        if not self.repo:
            return False

        try:
            current = self.repo.active_branch
            if branch_name in self.repo.heads:
                print(f"Branch {branch_name} already exists. Checking it out.")
                self.repo.heads[branch_name].checkout()
            else:
                print(f"Creating new branch {branch_name} from {current.name}")
                new_branch = self.repo.create_head(branch_name)
                new_branch.checkout()
            return True
        except Exception as e:
            print(f"Error creating branch: {e}")
            return False

    def commit_changes(self, message: str) -> bool:
        if not self.repo:
            return False

        try:
            if self.repo.is_dirty(untracked_files=True):
                self.repo.git.add(update=True)
                self.repo.git.add(".")
                self.repo.index.commit(message)
                print(f"Committed changes: {message}")
                return True
            else:
                print("No changes to commit.")
                return False
        except Exception as e:
            print(f"Error committing changes: {e}")
            return False

    def create_pr(self, title: str, body: str, token: Optional[str] = None) -> bool:
        """
        Creates a PR (or simulates it if no token/remote).
        """
        if not token:
            token = os.environ.get("GITHUB_TOKEN")

        if not token:
            print("GITHUB_TOKEN not found. Simulating PR creation.")
            print(f"Title: {title}")
            print(f"Body: {body}")
            return True

        if not self.repo:
            print("Not a git repository. Cannot create PR.")
            return False

        try:
            g = Github(token)
            # Need to find the repo name from remote
            # Simple heuristic: look at origin url
            remote_url = self.repo.remotes.origin.url
            # parse user/repo from url
            # git@github.com:user/repo.git or https://github.com/user/repo.git
            if "github.com" in remote_url:
                repo_name = remote_url.split("github.com")[-1].lstrip(":/").replace(".git", "")
                gh_repo = g.get_repo(repo_name)

                # Push the branch first
                current_branch = self.repo.active_branch.name
                self.repo.remotes.origin.push(current_branch)

                # Create PR
                pr = gh_repo.create_pull(
                    title=title,
                    body=body,
                    head=current_branch,
                    base=gh_repo.default_branch
                )
                print(f"PR created: {pr.html_url}")
                return True
            else:
                print("Remote is not GitHub. Cannot create PR.")
                return False

        except Exception as e:
            print(f"Error creating PR: {e}")
            return False
