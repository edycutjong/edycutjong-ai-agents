import streamlit as st
import pandas as pd
import altair as alt
import time
from datetime import datetime

# Adjust path to allow imports if run from root
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from agent.issue_tracker import IssueTracker
from agent.core import BugTriagerAgent

# --- Configuration & Setup ---
st.set_page_config(
    page_title="Auto Bug Triager",
    page_icon="🐞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'tracker' not in st.session_state:
    st.session_state.tracker = IssueTracker()
if 'agent' not in st.session_state:
    st.session_state.agent = BugTriagerAgent(st.session_state.tracker)

# --- Premium UI Styling (Royal Purple Theme) ---
st.markdown("""
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
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bug.png", width=60)
    st.title("Bug Triager AI")
    st.markdown("Automated triage & analysis system.")

    st.divider()

    page = st.radio("Navigation", ["Dashboard", "Issue Tracker", "New Issue"])

    st.divider()
    st.info(f"Mode: {'DEMO' if Config.DEMO_MODE else 'LIVE'}")
    if st.button("Run Stale Check"):
        with st.spinner("Checking for stale issues..."):
            count = st.session_state.agent.check_stale_issues()
            st.success(f"Marked {count} issues as stale.")
            time.sleep(1)
            st.rerun()

# --- Dashboard View ---
if page == "Dashboard":
    st.title("📊 Operational Dashboard")

    issues = st.session_state.tracker.get_all_issues()
    df = pd.DataFrame(issues)

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Issues", len(df))
    with col2:
        open_issues = len(df[df['status'] == 'open'])
        st.metric("Open Issues", open_issues, delta=f"{open_issues/len(df):.0%}" if len(df) > 0 else "0%")
    with col3:
        high_severity = len(df[df['severity'] == 'high']) + len(df[df['severity'] == 'critical'])
        st.metric("Critical/High", high_severity, delta_color="inverse")
    with col4:
        avg_sentiment = 0.5 # Placeholder if no sentiment data
        st.metric("Avg Sentiment", "Neutral")

    # Charts
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Severity Distribution")
        if not df.empty:
            chart = alt.Chart(df).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="severity", type="nominal", stack=True),
                color=alt.Color("severity", scale=alt.Scale(domain=['low', 'medium', 'high', 'critical'], range=['#4ade80', '#facc15', '#f87171', '#dc2626'])),
                tooltip=["severity", "count()"]
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)

    with col_chart2:
        st.subheader("Issues by Team")
        if not df.empty:
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("team", sort="-y"),
                y="count()",
                color=alt.Color("team", legend=None),
                tooltip=["team", "count()"]
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)

# --- Issue Tracker View ---
elif page == "Issue Tracker":
    st.title("🐞 Issue Tracker")

    issues = st.session_state.tracker.get_all_issues()
    df = pd.DataFrame(issues)

    # Filters
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    with col_filter1:
        status_filter = st.multiselect("Status", options=df['status'].unique(), default=df['status'].unique())
    with col_filter2:
        severity_filter = st.multiselect("Severity", options=df['severity'].unique(), default=df['severity'].unique())
    with col_filter3:
        team_filter = st.multiselect("Team", options=df['team'].unique(), default=df['team'].unique())

    # Apply filters
    filtered_df = df[
        (df['status'].isin(status_filter)) &
        (df['severity'].isin(severity_filter)) &
        (df['team'].isin(team_filter))
    ]

    # Display List
    st.dataframe(
        filtered_df[['id', 'title', 'severity', 'status', 'team', 'created_at']],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Issue Details
    issue_id_input = st.text_input("Enter Issue ID to view details", placeholder="ISSUE-101")
    if issue_id_input:
        issue = st.session_state.tracker.get_issue(issue_id_input)
        if issue:
            st.subheader(f"Details: {issue['title']}")

            detail_col1, detail_col2 = st.columns([2, 1])

            with detail_col1:
                st.markdown(f"**Description:**\n{issue['description']}")
                st.markdown(f"**AI Analysis:**\n```\n{issue['analysis']}\n```")

                if st.button("Generate Fix Suggestion"):
                    with st.spinner("Analyzing codebase..."):
                        suggestion = st.session_state.agent.suggest_fix(issue['id'])
                        st.success("Suggestion Generated!")
                        st.json(suggestion)

            with detail_col2:
                st.info(f"**Status:** {issue['status']}")
                st.warning(f"**Severity:** {issue['severity'].upper()}")
                st.success(f"**Team:** {issue['team']}")
                st.write(f"**Sentiment:** {issue['sentiment']}")
                st.write(f"**Labels:** {', '.join(issue['labels'])}")

                if st.button("Close Issue"):
                    st.session_state.tracker.update_issue(issue['id'], {"status": "closed"})
                    st.success("Issue closed!")
                    st.rerun()
        else:
            st.error("Issue not found.")

# --- New Issue View ---
elif page == "New Issue":
    st.title("📝 Report New Issue")

    with st.form("new_issue_form"):
        title = st.text_input("Issue Title")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Submit Issue")

        if submitted and title and description:
            with st.spinner("Triaging issue with AI..."):
                # Create issue
                new_issue = st.session_state.tracker.add_issue(title, description)

                # Analyze
                st.session_state.agent.analyze_issue(new_issue)

                st.success(f"Issue {new_issue['id']} created and triaged!")
                st.json(new_issue)
                time.sleep(2)
                st.rerun()
