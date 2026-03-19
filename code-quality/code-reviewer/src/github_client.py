import requests
from github import Github, GithubException
from agent_config import Config
from src.utils import logger, print_error

class GitHubClient:
    def __init__(self):
        try:
            Config.validate()
            self.github = Github(Config.GITHUB_TOKEN)
        except Exception as e:  # pragma: no cover
            logger.error(f"Failed to initialize GitHub client: {e}")  # pragma: no cover
            raise  # pragma: no cover

    def get_pr_diff(self, repo_name: str, pr_number: int) -> str:
        """Fetches the diff of a Pull Request."""
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            # Fetch the diff
            # PyGithub doesn't have a direct way to get the raw diff easily via get_pull object properties
            # that returns the string content directly in a unified diff format easily usable by LLMs usually.
            # However, we can use requests or access the diff_url.
            # Actually, requests.get(pr.diff_url) is the best way.
            headers = {'Authorization': f'token {Config.GITHUB_TOKEN}', 'Accept': 'application/vnd.github.v3.diff'}
            response = requests.get(pr.url, headers=headers)
            response.raise_for_status()
            return response.text
        except GithubException as e:  # pragma: no cover
            print_error(f"GitHub API Error: {e}")  # pragma: no cover
            logger.error(f"Error fetching PR diff: {e}")  # pragma: no cover
            raise  # pragma: no cover
        except Exception as e:  # pragma: no cover
            print_error(f"Error fetching PR diff: {e}")  # pragma: no cover
            logger.error(f"Unexpected error: {e}")  # pragma: no cover
            raise  # pragma: no cover

    def post_comment(self, repo_name: str, pr_number: int, body: str):
        """Posts a comment on a Pull Request."""
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(body)
            logger.info(f"Comment posted on PR #{pr_number} in {repo_name}")
        except GithubException as e:  # pragma: no cover
            print_error(f"GitHub API Error posting comment: {e}")  # pragma: no cover
            logger.error(f"Error posting comment: {e}")  # pragma: no cover
        except Exception as e:  # pragma: no cover
            print_error(f"Error posting comment: {e}")  # pragma: no cover
            logger.error(f"Unexpected error: {e}")  # pragma: no cover
