import streamlit as st
import os
import re
from dotenv import load_dotenv
from agent.github_client import GitHubClient, GithubException
from agent.reviewer import Reviewer
from config import Config

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="AI Code Review Automator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        background: -webkit-linear-gradient(45deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Cards */
    .css-1r6slb0, .stExpander {
        background-color: #1f2937;
        border-radius: 10px;
        border: 1px solid #374151;
        padding: 10px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(37, 117, 252, 0.4);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #374151;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to parse PR URL
def parse_pr_url(url):
    pattern = r"github\.com/([^/]+)/([^/]+)/pull/(\d+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1), match.group(2), int(match.group(3))
    return None, None, None

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    openai_api_key = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
    github_token = st.text_input("GitHub Token", value=os.getenv("GITHUB_TOKEN", ""), type="password")

    st.divider()

    st.subheader("Review Settings")
    review_focus = st.multiselect(
        "Focus Categories",
        ["Logic", "Security", "Style", "Performance", "Best Practices"],
        default=["Logic", "Security", "Style"]
    )

    guidelines = st.text_area(
        "Custom Guidelines",
        placeholder="e.g., verify variable naming conventions, ensure error handling...",
        height=150
    )

    st.info("Ensure you have provided valid API keys before starting.")

# Main Content
st.title("🤖 AI Code Review Automator")
st.markdown("### Intelligent Code Analysis & Review Assistant")

pr_url = st.text_input("Enter GitHub Pull Request URL", placeholder="https://github.com/owner/repo/pull/123")

# Initialize Session State
if "review_results" not in st.session_state:
    st.session_state.review_results = None
if "pr_details" not in st.session_state:
    st.session_state.pr_details = None

def run_review():
    if not openai_api_key or not github_token:
        st.error("Please provide both OpenAI API Key and GitHub Token.")
        return

    if not pr_url:
        st.error("Please enter a valid Pull Request URL.")
        return

    owner, repo_name, pr_number = parse_pr_url(pr_url)
    if not owner or not repo_name or not pr_number:
        st.error("Invalid PR URL format.")
        return

    full_repo_name = f"{owner}/{repo_name}"
    st.session_state.pr_details = {"repo": full_repo_name, "pr": pr_number}

    with st.status("Analyzing Pull Request...", expanded=True) as status:
        try:
            # Initialize Clients
            gh_client = GitHubClient(github_token)
            reviewer = Reviewer(openai_api_key)

            # Fetch Diff
            status.write("Fetching PR Diff from GitHub...")
            diff_data = gh_client.get_pr_diff(full_repo_name, pr_number)

            if not diff_data:
                status.update(label="No changes found or error fetching diff.", state="error")
                return

            status.write(f"Found {len(diff_data)} files changed. Analyzing code...")

            # Analyze Diff
            results = reviewer.analyze_diff(diff_data, guidelines, review_focus)
            st.session_state.review_results = results

            status.update(label="Review Complete!", state="complete", expanded=False)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            status.update(label="Error occurred", state="error")

# Action Buttons
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🚀 Start Review"):
        run_review()

# Display Results
if st.session_state.review_results:
    results = st.session_state.review_results
    summary = results.get("summary", "")
    comments = results.get("comments", [])

    st.divider()

    # Summary Section
    st.subheader("📝 Review Summary")
    st.markdown(f"<div style='background-color: #1f2937; padding: 20px; border-radius: 10px; border-left: 5px solid #6a11cb;'>{summary}</div>", unsafe_allow_html=True)

    st.divider()

    # Detailed Comments Section
    st.subheader(f"🔍 Detailed Findings ({len(comments)} issues)")

    if not comments:
        st.success("No major issues found based on the current criteria!")

    # Group comments by file
    files_comments = {}
    for comment in comments:
        fname = comment.get('filename')
        if fname not in files_comments:
            files_comments[fname] = []
        files_comments[fname].append(comment)

    for filename, file_issues in files_comments.items():
        with st.expander(f"📄 {filename} ({len(file_issues)} issues)"):
            for issue in file_issues:
                category = issue.get('category', 'General')
                line = issue.get('line', '?')
                body = issue.get('body', '')
                suggestion = issue.get('suggestion')

                # Determine color based on category
                color = "#3b82f6" # blue
                if "Security" in category:
                    color = "#ef4444" # red
                elif "Style" in category:
                    color = "#10b981" # green

                st.markdown(
                    f"""
                    <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #374151; border-radius: 5px;">
                        <span style="background-color: {color}; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold;">{category}</span>
                        <span style="margin-left: 10px; color: #9ca3af;">Line {line}</span>
                        <p style="margin-top: 5px;">{body}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if suggestion:
                    st.code(suggestion, language="python") # Defaulting to python syntax highlighting for now

    # Post to GitHub Section
    st.divider()
    st.subheader("📤 Submit Review")

    col_submit, col_cancel = st.columns([1, 4])
    with col_submit:
        if st.button("Post Comments to GitHub"):
            if not st.session_state.pr_details:
                st.error("No PR details found. Please run a review first.")
            else:
                try:
                    gh_client = GitHubClient(github_token)
                    repo = st.session_state.pr_details['repo']
                    pr_num = st.session_state.pr_details['pr']

                    with st.spinner("Posting comments..."):
                        # Post summary
                        gh_client.post_general_comment(repo, pr_num, f"### AI Review Summary\n\n{summary}")

                        # Post inline comments
                        # Note: We need the commit ID. We should have stored it or fetch it again.
                        # Ideally, verify_hallucinations or the diff fetcher should store the blob/sha.
                        # For now, we'll let post_review_comment fetch the latest head.
                        success_count = 0
                        for comment in comments:
                            try:
                                gh_client.post_review_comment(
                                    repo,
                                    pr_num,
                                    f"**[{comment.get('category')}]** {comment.get('body')}\n\nSuggested Fix:\n```\n{comment.get('suggestion', '')}\n```",
                                    comment.get('filename'),
                                    int(comment.get('line'))
                                )
                                success_count += 1
                            except Exception as e:
                                st.warning(f"Failed to post comment on {comment.get('filename')}:{comment.get('line')} - {e}")

                        st.success(f"Successfully posted {success_count} comments and the summary!")
                except Exception as e:
                    st.error(f"Failed to submit review: {e}")
