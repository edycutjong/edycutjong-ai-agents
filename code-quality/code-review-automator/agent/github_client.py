import github
from github import Github, GithubException
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubClient:
    def __init__(self, token: str):
        self.github = Github(token)
        self.user = self.github.get_user()

    def get_pr(self, repo_name: str, pr_number: int):
        """Fetches a Pull Request object."""
        try:
            repo = self.github.get_repo(repo_name)
            return repo.get_pull(pr_number)
        except GithubException as e:
            logger.error(f"Error fetching PR {repo_name}#{pr_number}: {e}")
            raise

    def get_pr_diff(self, repo_name: str, pr_number: int) -> List[Dict]:
        """
        Fetches the diff of a PR.
        Returns a list of dictionaries containing file path and patch (diff).
        """
        pr = self.get_pr(repo_name, pr_number)
        files = pr.get_files()
        diff_data = []

        for file in files:
            # Skip deleted files or files without patch (e.g. binary)
            if file.status == "removed" or not file.patch:
                continue

            diff_data.append({
                "filename": file.filename,
                "status": file.status,
                "patch": file.patch,
                "blob_url": file.blob_url,
                "sha": file.sha # verification
            })

        return diff_data

    def post_general_comment(self, repo_name: str, pr_number: int, body: str):
        """Posts a general comment on the PR (e.g., summary)."""
        pr = self.get_pr(repo_name, pr_number)
        try:
            pr.create_issue_comment(body)
            logger.info(f"Posted general comment on PR #{pr_number}")
        except GithubException as e:
            logger.error(f"Failed to post general comment: {e}")
            raise

    def post_review_comment(self, repo_name: str, pr_number: int, body: str, path: str, line: int, commit_id: str = None):
        """
        Posts a review comment on a specific line.
        Note: GitHub API requires 'position' (diff relative) or 'line' depending on the endpoint version.
        Using create_review_comment needs commit_id and position/line.
        Modern GitHub API allows creating a review with comments.
        """
        pr = self.get_pr(repo_name, pr_number)

        # If commit_id is not provided, use the head commit of the PR
        if not commit_id:
            commit_id = pr.head.sha

        # We need to find the correct side/commit.
        # Simple implementation: create a review comment.
        try:
            # Note: 'line' parameter in create_review_comment usually refers to the line in the file,
            # but sometimes it requires the position in the diff.
            # PyGithub/GitHub API behavior here can be tricky.
            # Using create_review is often safer for batching, but let's do single comments for now.

            # The 'line' parameter is the line number in the file (if side="RIGHT", which is default).
            # This requires the comment to be on a line that is part of the diff.
            pr.create_review_comment(body, commit_id, path, line=line)
            logger.info(f"Posted comment on {path}:{line}")
        except GithubException as e:
            logger.error(f"Failed to post review comment on {path}:{line}: {e}")
            # Fallback or specific error handling (e.g., if line is not in diff)
            logger.warning("Skipping comment as it might be outside the diff context.")

    def get_latest_commit_sha(self, repo_name: str, pr_number: int) -> str:
        pr = self.get_pr(repo_name, pr_number)
        return pr.head.sha
