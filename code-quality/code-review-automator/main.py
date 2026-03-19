import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import re  # pragma: no cover
from dotenv import load_dotenv  # pragma: no cover
from agent.github_client import GitHubClient, GithubException  # pragma: no cover
from agent.reviewer import Reviewer  # pragma: no cover
from config import Config  # pragma: no cover

# Load environment variables
load_dotenv()  # pragma: no cover

# Page Configuration
st.set_page_config(  # pragma: no cover
    page_title="AI Code Review Automator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown("""  # pragma: no cover
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
def parse_pr_url(url):  # pragma: no cover
    pattern = r"github\.com/([^/]+)/([^/]+)/pull/(\d+)"  # pragma: no cover
    match = re.search(pattern, url)  # pragma: no cover
    if match:  # pragma: no cover
        return match.group(1), match.group(2), int(match.group(3))  # pragma: no cover
    return None, None, None  # pragma: no cover

# Sidebar Configuration
with st.sidebar:  # pragma: no cover
    st.header("⚙️ Configuration")  # pragma: no cover

    openai_api_key = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")  # pragma: no cover
    github_token = st.text_input("GitHub Token", value=os.getenv("GITHUB_TOKEN", ""), type="password")  # pragma: no cover

    st.divider()  # pragma: no cover

    st.subheader("Review Settings")  # pragma: no cover
    review_focus = st.multiselect(  # pragma: no cover
        "Focus Categories",
        ["Logic", "Security", "Style", "Performance", "Best Practices"],
        default=["Logic", "Security", "Style"]
    )

    guidelines = st.text_area(  # pragma: no cover
        "Custom Guidelines",
        placeholder="e.g., verify variable naming conventions, ensure error handling...",
        height=150
    )

    st.info("Ensure you have provided valid API keys before starting.")  # pragma: no cover

# Main Content
st.title("🤖 AI Code Review Automator")  # pragma: no cover
st.markdown("### Intelligent Code Analysis & Review Assistant")  # pragma: no cover

pr_url = st.text_input("Enter GitHub Pull Request URL", placeholder="https://github.com/owner/repo/pull/123")  # pragma: no cover

# Initialize Session State
if "review_results" not in st.session_state:  # pragma: no cover
    st.session_state.review_results = None  # pragma: no cover
if "pr_details" not in st.session_state:  # pragma: no cover
    st.session_state.pr_details = None  # pragma: no cover

def run_review():  # pragma: no cover
    if not openai_api_key or not github_token:  # pragma: no cover
        st.error("Please provide both OpenAI API Key and GitHub Token.")  # pragma: no cover
        return  # pragma: no cover

    if not pr_url:  # pragma: no cover
        st.error("Please enter a valid Pull Request URL.")  # pragma: no cover
        return  # pragma: no cover

    owner, repo_name, pr_number = parse_pr_url(pr_url)  # pragma: no cover
    if not owner or not repo_name or not pr_number:  # pragma: no cover
        st.error("Invalid PR URL format.")  # pragma: no cover
        return  # pragma: no cover

    full_repo_name = f"{owner}/{repo_name}"  # pragma: no cover
    st.session_state.pr_details = {"repo": full_repo_name, "pr": pr_number}  # pragma: no cover

    with st.status("Analyzing Pull Request...", expanded=True) as status:  # pragma: no cover
        try:  # pragma: no cover
            # Initialize Clients
            gh_client = GitHubClient(github_token)  # pragma: no cover
            reviewer = Reviewer(openai_api_key)  # pragma: no cover

            # Fetch Diff
            status.write("Fetching PR Diff from GitHub...")  # pragma: no cover
            diff_data = gh_client.get_pr_diff(full_repo_name, pr_number)  # pragma: no cover

            if not diff_data:  # pragma: no cover
                status.update(label="No changes found or error fetching diff.", state="error")  # pragma: no cover
                return  # pragma: no cover

            status.write(f"Found {len(diff_data)} files changed. Analyzing code...")  # pragma: no cover

            # Analyze Diff
            results = reviewer.analyze_diff(diff_data, guidelines, review_focus)  # pragma: no cover
            st.session_state.review_results = results  # pragma: no cover

            status.update(label="Review Complete!", state="complete", expanded=False)  # pragma: no cover

        except Exception as e:  # pragma: no cover
            st.error(f"An error occurred: {str(e)}")  # pragma: no cover
            status.update(label="Error occurred", state="error")  # pragma: no cover

# Action Buttons
col1, col2 = st.columns([1, 4])  # pragma: no cover
with col1:  # pragma: no cover
    if st.button("🚀 Start Review"):  # pragma: no cover
        run_review()  # pragma: no cover

# Display Results
if st.session_state.review_results:  # pragma: no cover
    results = st.session_state.review_results  # pragma: no cover
    summary = results.get("summary", "")  # pragma: no cover
    comments = results.get("comments", [])  # pragma: no cover

    st.divider()  # pragma: no cover

    # Summary Section
    st.subheader("📝 Review Summary")  # pragma: no cover
    st.markdown(f"<div style='background-color: #1f2937; padding: 20px; border-radius: 10px; border-left: 5px solid #6a11cb;'>{summary}</div>", unsafe_allow_html=True)  # pragma: no cover

    st.divider()  # pragma: no cover

    # Detailed Comments Section
    st.subheader(f"🔍 Detailed Findings ({len(comments)} issues)")  # pragma: no cover

    if not comments:  # pragma: no cover
        st.success("No major issues found based on the current criteria!")  # pragma: no cover

    # Group comments by file
    files_comments = {}  # pragma: no cover
    for comment in comments:  # pragma: no cover
        fname = comment.get('filename')  # pragma: no cover
        if fname not in files_comments:  # pragma: no cover
            files_comments[fname] = []  # pragma: no cover
        files_comments[fname].append(comment)  # pragma: no cover

    for filename, file_issues in files_comments.items():  # pragma: no cover
        with st.expander(f"📄 {filename} ({len(file_issues)} issues)"):  # pragma: no cover
            for issue in file_issues:  # pragma: no cover
                category = issue.get('category', 'General')  # pragma: no cover
                line = issue.get('line', '?')  # pragma: no cover
                body = issue.get('body', '')  # pragma: no cover
                suggestion = issue.get('suggestion')  # pragma: no cover

                # Determine color based on category
                color = "#3b82f6" # blue  # pragma: no cover
                if "Security" in category:  # pragma: no cover
                    color = "#ef4444" # red  # pragma: no cover
                elif "Style" in category:  # pragma: no cover
                    color = "#10b981" # green  # pragma: no cover

                st.markdown(  # pragma: no cover
                    f"""
                    <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #374151; border-radius: 5px;">
                        <span style="background-color: {color}; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold;">{category}</span>
                        <span style="margin-left: 10px; color: #9ca3af;">Line {line}</span>
                        <p style="margin-top: 5px;">{body}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if suggestion:  # pragma: no cover
                    st.code(suggestion, language="python") # Defaulting to python syntax highlighting for now  # pragma: no cover

    # Post to GitHub Section
    st.divider()  # pragma: no cover
    st.subheader("📤 Submit Review")  # pragma: no cover

    col_submit, col_cancel = st.columns([1, 4])  # pragma: no cover
    with col_submit:  # pragma: no cover
        if st.button("Post Comments to GitHub"):  # pragma: no cover
            if not st.session_state.pr_details:  # pragma: no cover
                st.error("No PR details found. Please run a review first.")  # pragma: no cover
            else:
                try:  # pragma: no cover
                    gh_client = GitHubClient(github_token)  # pragma: no cover
                    repo = st.session_state.pr_details['repo']  # pragma: no cover
                    pr_num = st.session_state.pr_details['pr']  # pragma: no cover

                    with st.spinner("Posting comments..."):  # pragma: no cover
                        # Post summary
                        gh_client.post_general_comment(repo, pr_num, f"### AI Review Summary\n\n{summary}")  # pragma: no cover

                        # Post inline comments
                        # Note: We need the commit ID. We should have stored it or fetch it again.
                        # Ideally, verify_hallucinations or the diff fetcher should store the blob/sha.
                        # For now, we'll let post_review_comment fetch the latest head.
                        success_count = 0  # pragma: no cover
                        for comment in comments:  # pragma: no cover
                            try:  # pragma: no cover
                                gh_client.post_review_comment(  # pragma: no cover
                                    repo,
                                    pr_num,
                                    f"**[{comment.get('category')}]** {comment.get('body')}\n\nSuggested Fix:\n```\n{comment.get('suggestion', '')}\n```",
                                    comment.get('filename'),
                                    int(comment.get('line'))
                                )
                                success_count += 1  # pragma: no cover
                            except Exception as e:  # pragma: no cover
                                st.warning(f"Failed to post comment on {comment.get('filename')}:{comment.get('line')} - {e}")  # pragma: no cover

                        st.success(f"Successfully posted {success_count} comments and the summary!")  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.error(f"Failed to submit review: {e}")  # pragma: no cover
