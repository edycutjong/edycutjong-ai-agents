from git import Repo, GitCommandError
import os

class GitHandler:
    def __init__(self, repo_path: str):
        self.repo_path = os.path.abspath(repo_path)
        try:
            self.repo = Repo(self.repo_path)
        except Exception:
            self.repo = None # Not a git repo

    def is_git_repo(self) -> bool:
        return self.repo is not None

    def has_changes(self) -> bool:
        if not self.is_git_repo():
            return False
        return self.repo.is_dirty(untracked_files=True)

    def commit_changes(self, message: str) -> bool:
        if not self.is_git_repo():
            return False

        try:
            # Stage all changes
            self.repo.git.add(A=True)
            # Commit
            self.repo.index.commit(message)
            return True
        except GitCommandError as e:
            print(f"Git error: {e}")
            return False
        except Exception as e:
            print(f"Error committing: {e}")
            return False
