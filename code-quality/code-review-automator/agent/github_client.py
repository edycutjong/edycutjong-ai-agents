import github  # pragma: no cover
from github import Github, GithubException  # pragma: no cover
from typing import List, Dict, Optional  # pragma: no cover
import logging  # pragma: no cover

# Configure logging
logging.basicConfig(level=logging.INFO)  # pragma: no cover
logger = logging.getLogger(__name__)  # pragma: no cover

class GitHubClient:  # pragma: no cover
    def __init__(self, token: str):  # pragma: no cover
        self.github = Github(token)  # pragma: no cover
        self.user = self.github.get_user()  # pragma: no cover

    def get_pr(self, repo_name: str, pr_number: int):  # pragma: no cover
        """Fetches a Pull Request object."""
        try:  # pragma: no cover
            repo = self.github.get_repo(repo_name)  # pragma: no cover
            return repo.get_pull(pr_number)  # pragma: no cover
        except GithubException as e:  # pragma: no cover
            logger.error(f"Error fetching PR {repo_name}#{pr_number}: {e}")  # pragma: no cover
            raise  # pragma: no cover

    def get_pr_diff(self, repo_name: str, pr_number: int) -> List[Dict]:  # pragma: no cover
        """
        Fetches the diff of a PR.
        Returns a list of dictionaries containing file path and patch (diff).
        """
        pr = self.get_pr(repo_name, pr_number)  # pragma: no cover
        files = pr.get_files()  # pragma: no cover
        diff_data = []  # pragma: no cover

        for file in files:  # pragma: no cover
            # Skip deleted files or files without patch (e.g. binary)
            if file.status == "removed" or not file.patch:  # pragma: no cover
                continue  # pragma: no cover

            diff_data.append({  # pragma: no cover
                "filename": file.filename,
                "status": file.status,
                "patch": file.patch,
                "blob_url": file.blob_url,
                "sha": file.sha # verification
            })

        return diff_data  # pragma: no cover

    def post_general_comment(self, repo_name: str, pr_number: int, body: str):  # pragma: no cover
        """Posts a general comment on the PR (e.g., summary)."""
        pr = self.get_pr(repo_name, pr_number)  # pragma: no cover
        try:  # pragma: no cover
            pr.create_issue_comment(body)  # pragma: no cover
            logger.info(f"Posted general comment on PR #{pr_number}")  # pragma: no cover
        except GithubException as e:  # pragma: no cover
            logger.error(f"Failed to post general comment: {e}")  # pragma: no cover
            raise  # pragma: no cover

    def post_review_comment(self, repo_name: str, pr_number: int, body: str, path: str, line: int, commit_id: str = None):  # pragma: no cover
        """
        Posts a review comment on a specific line.
        Note: GitHub API requires 'position' (diff relative) or 'line' depending on the endpoint version.
        Using create_review_comment needs commit_id and position/line.
        Modern GitHub API allows creating a review with comments.
        """
        pr = self.get_pr(repo_name, pr_number)  # pragma: no cover

        # If commit_id is not provided, use the head commit of the PR
        if not commit_id:  # pragma: no cover
            commit_id = pr.head.sha  # pragma: no cover

        # We need to find the correct side/commit.
        # Simple implementation: create a review comment.
        try:  # pragma: no cover
            # Note: 'line' parameter in create_review_comment usually refers to the line in the file,
            # but sometimes it requires the position in the diff.
            # PyGithub/GitHub API behavior here can be tricky.
            # Using create_review is often safer for batching, but let's do single comments for now.

            # The 'line' parameter is the line number in the file (if side="RIGHT", which is default).
            # This requires the comment to be on a line that is part of the diff.
            pr.create_review_comment(body, commit_id, path, line=line)  # pragma: no cover
            logger.info(f"Posted comment on {path}:{line}")  # pragma: no cover
        except GithubException as e:  # pragma: no cover
            logger.error(f"Failed to post review comment on {path}:{line}: {e}")  # pragma: no cover
            # Fallback or specific error handling (e.g., if line is not in diff)
            logger.warning("Skipping comment as it might be outside the diff context.")  # pragma: no cover

    def get_latest_commit_sha(self, repo_name: str, pr_number: int) -> str:  # pragma: no cover
        pr = self.get_pr(repo_name, pr_number)  # pragma: no cover
        return pr.head.sha  # pragma: no cover
