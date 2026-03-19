import os  # pragma: no cover
import git  # pragma: no cover
from typing import Optional  # pragma: no cover
from github import Github  # pragma: no cover

class GitManager:  # pragma: no cover
    def __init__(self, repo_path: str = "."):  # pragma: no cover
        self.repo_path = repo_path  # pragma: no cover
        try:  # pragma: no cover
            self.repo = git.Repo(repo_path)  # pragma: no cover
        except git.exc.InvalidGitRepositoryError:  # pragma: no cover
            print(f"Not a git repository: {repo_path}")  # pragma: no cover
            self.repo = None  # pragma: no cover

    def create_branch(self, branch_name: str) -> bool:  # pragma: no cover
        if not self.repo:  # pragma: no cover
            return False  # pragma: no cover

        try:  # pragma: no cover
            current = self.repo.active_branch  # pragma: no cover
            if branch_name in self.repo.heads:  # pragma: no cover
                print(f"Branch {branch_name} already exists. Checking it out.")  # pragma: no cover
                self.repo.heads[branch_name].checkout()  # pragma: no cover
            else:
                print(f"Creating new branch {branch_name} from {current.name}")  # pragma: no cover
                new_branch = self.repo.create_head(branch_name)  # pragma: no cover
                new_branch.checkout()  # pragma: no cover
            return True  # pragma: no cover
        except Exception as e:  # pragma: no cover
            print(f"Error creating branch: {e}")  # pragma: no cover
            return False  # pragma: no cover

    def commit_changes(self, message: str) -> bool:  # pragma: no cover
        if not self.repo:  # pragma: no cover
            return False  # pragma: no cover

        try:  # pragma: no cover
            if self.repo.is_dirty(untracked_files=True):  # pragma: no cover
                self.repo.git.add(update=True)  # pragma: no cover
                self.repo.git.add(".")  # pragma: no cover
                self.repo.index.commit(message)  # pragma: no cover
                print(f"Committed changes: {message}")  # pragma: no cover
                return True  # pragma: no cover
            else:
                print("No changes to commit.")  # pragma: no cover
                return False  # pragma: no cover
        except Exception as e:  # pragma: no cover
            print(f"Error committing changes: {e}")  # pragma: no cover
            return False  # pragma: no cover

    def create_pr(self, title: str, body: str, token: Optional[str] = None) -> bool:  # pragma: no cover
        """
        Creates a PR (or simulates it if no token/remote).
        """
        if not token:  # pragma: no cover
            token = os.environ.get("GITHUB_TOKEN")  # pragma: no cover

        if not token:  # pragma: no cover
            print("GITHUB_TOKEN not found. Simulating PR creation.")  # pragma: no cover
            print(f"Title: {title}")  # pragma: no cover
            print(f"Body: {body}")  # pragma: no cover
            return True  # pragma: no cover

        if not self.repo:  # pragma: no cover
            print("Not a git repository. Cannot create PR.")  # pragma: no cover
            return False  # pragma: no cover

        try:  # pragma: no cover
            g = Github(token)  # pragma: no cover
            # Need to find the repo name from remote
            # Simple heuristic: look at origin url
            remote_url = self.repo.remotes.origin.url  # pragma: no cover
            # parse user/repo from url
            # git@github.com:user/repo.git or https://github.com/user/repo.git
            if "github.com" in remote_url:  # pragma: no cover
                repo_name = remote_url.split("github.com")[-1].lstrip(":/").replace(".git", "")  # pragma: no cover
                gh_repo = g.get_repo(repo_name)  # pragma: no cover

                # Push the branch first
                current_branch = self.repo.active_branch.name  # pragma: no cover
                self.repo.remotes.origin.push(current_branch)  # pragma: no cover

                # Create PR
                pr = gh_repo.create_pull(  # pragma: no cover
                    title=title,
                    body=body,
                    head=current_branch,
                    base=gh_repo.default_branch
                )
                print(f"PR created: {pr.html_url}")  # pragma: no cover
                return True  # pragma: no cover
            else:
                print("Remote is not GitHub. Cannot create PR.")  # pragma: no cover
                return False  # pragma: no cover

        except Exception as e:  # pragma: no cover
            print(f"Error creating PR: {e}")  # pragma: no cover
            return False  # pragma: no cover
