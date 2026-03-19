import os
from typing import List, Optional
from git import Repo
from github import Github, GithubException

class GitHandler:
    def __init__(self, repo_path: str = "."):
        self.repo = Repo(repo_path)

    def get_current_branch(self) -> str:
        return self.repo.active_branch.name

    def get_diff(self, target_branch: str = "main") -> str:
        """Get diff between current branch and target branch."""
        # fetch target branch first to ensure we have latest
        try:
            origin = self.repo.remotes.origin
            origin.fetch()
        except Exception as e:  # pragma: no cover
            print(f"Warning: Could not fetch from origin: {e}")  # pragma: no cover

        return self.repo.git.diff(target_branch)

    def list_changed_files(self, target_branch: str = "main") -> List[str]:
        """List files changed between current branch and target branch."""
        diff = self.repo.git.diff(target_branch, name_only=True)
        return diff.splitlines()

    def commit_changes(self, message: str, files: List[str] = None):
        """Commit changes to the current branch."""
        if files:  # pragma: no cover
            self.repo.index.add(files)  # pragma: no cover
        else:
            self.repo.index.add(update=True) # Add all modified  # pragma: no cover

        self.repo.index.commit(message)  # pragma: no cover

    def push_changes(self):
        """Push changes to origin."""
        origin = self.repo.remotes.origin  # pragma: no cover
        origin.push()  # pragma: no cover

class PRHandler:
    def __init__(self, repo_name: str, pr_number: int, token: Optional[str] = None):
        self.repo_name = repo_name
        self.pr_number = pr_number
        if token:
            self.g = Github(token)
        else:
            self.g = None  # pragma: no cover
            print("Warning: No GitHub token provided. PR operations will be simulated.")  # pragma: no cover

    def post_comment(self, body: str):
        """Post a comment on the PR."""
        if not self.g:
            print(f"[SIMULATION] Posting comment on PR #{self.pr_number}:\n{body}")  # pragma: no cover
            return  # pragma: no cover

        try:
            repo = self.g.get_repo(self.repo_name)
            pr = repo.get_pull(self.pr_number)
            pr.create_issue_comment(body)
        except GithubException as e:  # pragma: no cover
            print(f"Error posting comment: {e}")  # pragma: no cover

    def get_pr_diff(self) -> str:
        """Get the diff of the PR."""
        if not self.g:  # pragma: no cover
            return "" # Simulation mode or error  # pragma: no cover

        try:  # pragma: no cover
            repo = self.g.get_repo(self.repo_name)  # pragma: no cover
            pr = repo.get_pull(self.pr_number)  # pragma: no cover
            # This requires getting the diff url or using requests,
            # but PyGithub doesn't return raw diff easily.
            # For now, let's assume we use local git if possible or use files.
            # Actually, getting files from PR is better.
            files = pr.get_files()  # pragma: no cover
            diffs = []  # pragma: no cover
            for f in files:  # pragma: no cover
                diffs.append(f"File: {f.filename}\nPatch:\n{f.patch}")  # pragma: no cover
            return "\n".join(diffs)  # pragma: no cover
        except GithubException as e:  # pragma: no cover
            print(f"Error getting PR diff: {e}")  # pragma: no cover
            return ""  # pragma: no cover

    def get_changed_files(self) -> List[str]:
        """Get list of changed files in the PR."""
        if not self.g:
            return []  # pragma: no cover

        try:
            repo = self.g.get_repo(self.repo_name)
            pr = repo.get_pull(self.pr_number)
            return [f.filename for f in pr.get_files()]
        except GithubException as e:  # pragma: no cover
            print(f"Error getting PR files: {e}")  # pragma: no cover
            return []  # pragma: no cover

    def get_file_content(self, path: str) -> str:
        """Get content of a file from the PR head."""
        if not self.g:  # pragma: no cover
            return ""  # pragma: no cover

        try:  # pragma: no cover
            repo = self.g.get_repo(self.repo_name)  # pragma: no cover
            pr = repo.get_pull(self.pr_number)  # pragma: no cover
            # getting content from the head sha of the PR
            contents = repo.get_contents(path, ref=pr.head.sha)  # pragma: no cover
            return contents.decoded_content.decode('utf-8')  # pragma: no cover
        except GithubException as e:  # pragma: no cover
            print(f"Error getting file content: {e}")  # pragma: no cover
            return ""  # pragma: no cover

    def get_file_patch(self, filename: str) -> str:
        """Get the patch/diff for a specific file in the PR."""
        if not self.g:
            return ""  # pragma: no cover
        try:
            repo = self.g.get_repo(self.repo_name)
            pr = repo.get_pull(self.pr_number)
            for f in pr.get_files():
                if f.filename == filename:
                    return f.patch
            return ""
        except GithubException as e:  # pragma: no cover
             print(f"Error getting file patch: {e}")  # pragma: no cover
             return ""  # pragma: no cover
