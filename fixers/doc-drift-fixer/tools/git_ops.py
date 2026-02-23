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
        except Exception as e:
            print(f"Warning: Could not fetch from origin: {e}")

        return self.repo.git.diff(target_branch)

    def list_changed_files(self, target_branch: str = "main") -> List[str]:
        """List files changed between current branch and target branch."""
        diff = self.repo.git.diff(target_branch, name_only=True)
        return diff.splitlines()

    def commit_changes(self, message: str, files: List[str] = None):
        """Commit changes to the current branch."""
        if files:
            self.repo.index.add(files)
        else:
            self.repo.index.add(update=True) # Add all modified

        self.repo.index.commit(message)

    def push_changes(self):
        """Push changes to origin."""
        origin = self.repo.remotes.origin
        origin.push()

class PRHandler:
    def __init__(self, repo_name: str, pr_number: int, token: Optional[str] = None):
        self.repo_name = repo_name
        self.pr_number = pr_number
        if token:
            self.g = Github(token)
        else:
            self.g = None
            print("Warning: No GitHub token provided. PR operations will be simulated.")

    def post_comment(self, body: str):
        """Post a comment on the PR."""
        if not self.g:
            print(f"[SIMULATION] Posting comment on PR #{self.pr_number}:\n{body}")
            return

        try:
            repo = self.g.get_repo(self.repo_name)
            pr = repo.get_pull(self.pr_number)
            pr.create_issue_comment(body)
        except GithubException as e:
            print(f"Error posting comment: {e}")

    def get_pr_diff(self) -> str:
        """Get the diff of the PR."""
        if not self.g:
            return "" # Simulation mode or error

        try:
            repo = self.g.get_repo(self.repo_name)
            pr = repo.get_pull(self.pr_number)
            # This requires getting the diff url or using requests,
            # but PyGithub doesn't return raw diff easily.
            # For now, let's assume we use local git if possible or use files.
            # Actually, getting files from PR is better.
            files = pr.get_files()
            diffs = []
            for f in files:
                diffs.append(f"File: {f.filename}\nPatch:\n{f.patch}")
            return "\n".join(diffs)
        except GithubException as e:
            print(f"Error getting PR diff: {e}")
            return ""

    def get_changed_files(self) -> List[str]:
        """Get list of changed files in the PR."""
        if not self.g:
            return []

        try:
            repo = self.g.get_repo(self.repo_name)
            pr = repo.get_pull(self.pr_number)
            return [f.filename for f in pr.get_files()]
        except GithubException as e:
            print(f"Error getting PR files: {e}")
            return []

    def get_file_content(self, path: str) -> str:
        """Get content of a file from the PR head."""
        if not self.g:
            return ""

        try:
            repo = self.g.get_repo(self.repo_name)
            pr = repo.get_pull(self.pr_number)
            # getting content from the head sha of the PR
            contents = repo.get_contents(path, ref=pr.head.sha)
            return contents.decoded_content.decode('utf-8')
        except GithubException as e:
            print(f"Error getting file content: {e}")
            return ""

    def get_file_patch(self, filename: str) -> str:
        """Get the patch/diff for a specific file in the PR."""
        if not self.g:
            return ""
        try:
            repo = self.g.get_repo(self.repo_name)
            pr = repo.get_pull(self.pr_number)
            for f in pr.get_files():
                if f.filename == filename:
                    return f.patch
            return ""
        except GithubException as e:
             print(f"Error getting file patch: {e}")
             return ""
