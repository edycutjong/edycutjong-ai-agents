import streamlit as st  # pragma: no cover
import pandas as pd  # pragma: no cover
import altair as alt  # pragma: no cover
import time  # pragma: no cover
from datetime import datetime  # pragma: no cover

# Adjust path to allow imports if run from root
import sys  # pragma: no cover
import os  # pragma: no cover
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover

from config import Config  # pragma: no cover
from agent.issue_tracker import IssueTracker  # pragma: no cover
from agent.core import BugTriagerAgent  # pragma: no cover

# --- Configuration & Setup ---
st.set_page_config(  # pragma: no cover
    page_title="Auto Bug Triager",
    page_icon="🐞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'tracker' not in st.session_state:  # pragma: no cover
    st.session_state.tracker = IssueTracker()  # pragma: no cover
if 'agent' not in st.session_state:  # pragma: no cover
    st.session_state.agent = BugTriagerAgent(st.session_state.tracker)  # pragma: no cover

# --- Premium UI Styling (Royal Purple Theme) ---
st.markdown("""  # pragma: no cover
    <style>
    /* Global Styles */
    .stApp {
        background-color: #0f0c29; /* Dark background */
        background-image: linear-gradient(315deg, #0f0c29 0%, #302b63 74%, #24243e 100%);
        color: #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Headings */
    h1, h2, h3 {
        color: #DDD6FE !important; /* Accent */
        font-weight: 700;
    }

    /* Metrics */
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Force metric text color */
    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] {
        color: #e0e0e0 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #8B5CF6 0%, #6366F1 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    }

    /* Dataframes */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e1b4b;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Cards */
    .css-card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:  # pragma: no cover
    st.image("https://img.icons8.com/fluency/96/bug.png", width=60)  # pragma: no cover
    st.title("Bug Triager AI")  # pragma: no cover
    st.markdown("Automated triage & analysis system.")  # pragma: no cover

    st.divider()  # pragma: no cover

    page = st.radio("Navigation", ["Dashboard", "Issue Tracker", "New Issue"])  # pragma: no cover

    st.divider()  # pragma: no cover
    st.info(f"Mode: {'DEMO' if Config.DEMO_MODE else 'LIVE'}")  # pragma: no cover
    if st.button("Run Stale Check"):  # pragma: no cover
        with st.spinner("Checking for stale issues..."):  # pragma: no cover
            count = st.session_state.agent.check_stale_issues()  # pragma: no cover
            st.success(f"Marked {count} issues as stale.")  # pragma: no cover
            time.sleep(1)  # pragma: no cover
            st.rerun()  # pragma: no cover

# --- Dashboard View ---
if page == "Dashboard":  # pragma: no cover
    st.title("📊 Operational Dashboard")  # pragma: no cover

    issues = st.session_state.tracker.get_all_issues()  # pragma: no cover
    df = pd.DataFrame(issues)  # pragma: no cover

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)  # pragma: no cover
    with col1:  # pragma: no cover
        st.metric("Total Issues", len(df))  # pragma: no cover
    with col2:  # pragma: no cover
        open_issues = len(df[df['status'] == 'open'])  # pragma: no cover
        st.metric("Open Issues", open_issues, delta=f"{open_issues/len(df):.0%}" if len(df) > 0 else "0%")  # pragma: no cover
    with col3:  # pragma: no cover
        high_severity = len(df[df['severity'] == 'high']) + len(df[df['severity'] == 'critical'])  # pragma: no cover
        st.metric("Critical/High", high_severity, delta_color="inverse")  # pragma: no cover
    with col4:  # pragma: no cover
        avg_sentiment = 0.5 # Placeholder if no sentiment data  # pragma: no cover
        st.metric("Avg Sentiment", "Neutral")  # pragma: no cover

    # Charts
    col_chart1, col_chart2 = st.columns(2)  # pragma: no cover

    with col_chart1:  # pragma: no cover
        st.subheader("Severity Distribution")  # pragma: no cover
        if not df.empty:  # pragma: no cover
            chart = alt.Chart(df).mark_arc(innerRadius=50).encode(  # pragma: no cover
                theta=alt.Theta(field="severity", type="nominal", stack=True),
                color=alt.Color("severity", scale=alt.Scale(domain=['low', 'medium', 'high', 'critical'], range=['#4ade80', '#facc15', '#f87171', '#dc2626'])),
                tooltip=["severity", "count()"]
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)  # pragma: no cover

    with col_chart2:  # pragma: no cover
        st.subheader("Issues by Team")  # pragma: no cover
        if not df.empty:  # pragma: no cover
            chart = alt.Chart(df).mark_bar().encode(  # pragma: no cover
                x=alt.X("team", sort="-y"),
                y="count()",
                color=alt.Color("team", legend=None),
                tooltip=["team", "count()"]
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)  # pragma: no cover

# --- Issue Tracker View ---
elif page == "Issue Tracker":  # pragma: no cover
    st.title("🐞 Issue Tracker")  # pragma: no cover

    issues = st.session_state.tracker.get_all_issues()  # pragma: no cover
    df = pd.DataFrame(issues)  # pragma: no cover

    # Filters
    col_filter1, col_filter2, col_filter3 = st.columns(3)  # pragma: no cover
    with col_filter1:  # pragma: no cover
        status_filter = st.multiselect("Status", options=df['status'].unique(), default=df['status'].unique())  # pragma: no cover
    with col_filter2:  # pragma: no cover
        severity_filter = st.multiselect("Severity", options=df['severity'].unique(), default=df['severity'].unique())  # pragma: no cover
    with col_filter3:  # pragma: no cover
        team_filter = st.multiselect("Team", options=df['team'].unique(), default=df['team'].unique())  # pragma: no cover

    # Apply filters
    filtered_df = df[  # pragma: no cover
        (df['status'].isin(status_filter)) &
        (df['severity'].isin(severity_filter)) &
        (df['team'].isin(team_filter))
    ]

    # Display List
    st.dataframe(  # pragma: no cover
        filtered_df[['id', 'title', 'severity', 'status', 'team', 'created_at']],
        use_container_width=True,
        hide_index=True
    )

    st.divider()  # pragma: no cover

    # Issue Details
    issue_id_input = st.text_input("Enter Issue ID to view details", placeholder="ISSUE-101")  # pragma: no cover
    if issue_id_input:  # pragma: no cover
        issue = st.session_state.tracker.get_issue(issue_id_input)  # pragma: no cover
        if issue:  # pragma: no cover
            st.subheader(f"Details: {issue['title']}")  # pragma: no cover

            detail_col1, detail_col2 = st.columns([2, 1])  # pragma: no cover

            with detail_col1:  # pragma: no cover
                st.markdown(f"**Description:**\n{issue['description']}")  # pragma: no cover
                st.markdown(f"**AI Analysis:**\n```\n{issue['analysis']}\n```")  # pragma: no cover

                if st.button("Generate Fix Suggestion"):  # pragma: no cover
                    with st.spinner("Analyzing codebase..."):  # pragma: no cover
                        suggestion = st.session_state.agent.suggest_fix(issue['id'])  # pragma: no cover
                        st.success("Suggestion Generated!")  # pragma: no cover
                        st.json(suggestion)  # pragma: no cover

            with detail_col2:  # pragma: no cover
                st.info(f"**Status:** {issue['status']}")  # pragma: no cover
                st.warning(f"**Severity:** {issue['severity'].upper()}")  # pragma: no cover
                st.success(f"**Team:** {issue['team']}")  # pragma: no cover
                st.write(f"**Sentiment:** {issue['sentiment']}")  # pragma: no cover
                st.write(f"**Labels:** {', '.join(issue['labels'])}")  # pragma: no cover

                if st.button("Close Issue"):  # pragma: no cover
                    st.session_state.tracker.update_issue(issue['id'], {"status": "closed"})  # pragma: no cover
                    st.success("Issue closed!")  # pragma: no cover
                    st.rerun()  # pragma: no cover
        else:
            st.error("Issue not found.")  # pragma: no cover

# --- New Issue View ---
elif page == "New Issue":  # pragma: no cover
    st.title("📝 Report New Issue")  # pragma: no cover

    with st.form("new_issue_form"):  # pragma: no cover
        title = st.text_input("Issue Title")  # pragma: no cover
        description = st.text_area("Description")  # pragma: no cover
        submitted = st.form_submit_button("Submit Issue")  # pragma: no cover

        if submitted and title and description:  # pragma: no cover
            with st.spinner("Triaging issue with AI..."):  # pragma: no cover
                # Create issue
                new_issue = st.session_state.tracker.add_issue(title, description)  # pragma: no cover

                # Analyze
                st.session_state.agent.analyze_issue(new_issue)  # pragma: no cover

                st.success(f"Issue {new_issue['id']} created and triaged!")  # pragma: no cover
                st.json(new_issue)  # pragma: no cover
                time.sleep(2)  # pragma: no cover
                st.rerun()  # pragma: no cover
