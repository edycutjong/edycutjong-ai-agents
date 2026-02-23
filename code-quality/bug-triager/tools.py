from github import Github, GithubException
from crewai.tools import tool
from agent_config import Config

# Helper functions for main.py (not necessarily agent tools)

def get_github_client():
    return Github(Config.GITHUB_TOKEN)

def get_repo():
    g = get_github_client()
    return g.get_repo(Config.GITHUB_REPO)

def fetch_open_issues():
    """Fetches all open issues from the repository."""
    repo = get_repo()
    return repo.get_issues(state='open')

def apply_label(issue_number: int, label: str):
    """Adds a label to an issue."""
    repo = get_repo()
    issue = repo.get_issue(issue_number)
    try:
        issue.add_to_labels(label)
        return True
    except GithubException as e:
        print(f"Error adding label: {e}")
        return False

def assign_user(issue_number: int, username: str):
    """Assigns a user to an issue."""
    repo = get_repo()
    issue = repo.get_issue(issue_number)
    try:
        issue.add_to_assignees(username)
        return True
    except GithubException as e:
        print(f"Error assigning user: {e}")
        return False

def post_comment(issue_number: int, body: str):
    """Posts a comment to an issue."""
    repo = get_repo()
    issue = repo.get_issue(issue_number)
    try:
        issue.create_comment(body)
        return True
    except GithubException as e:
        print(f"Error posting comment: {e}")
        return False

# Agent Tools

@tool("Search Similar Issues")
def search_similar_issues(query: str):
    """Searches for existing closed or open issues that are similar to the given query string.
    Useful for finding duplicates."""
    try:
        g = Github(Config.GITHUB_TOKEN)
        # Search query syntax: "repo:owner/repo query"
        search_query = f"repo:{Config.GITHUB_REPO} {query}"
        results = g.search_issues(query=search_query)

        issues_found = []
        for issue in results[:5]: # Limit to 5 results
            issues_found.append(f"Issue #{issue.number}: {issue.title} (State: {issue.state})")

        if not issues_found:
            return "No similar issues found."
        return "\n".join(issues_found)
    except Exception as e:
        return f"Error searching issues: {str(e)}"
