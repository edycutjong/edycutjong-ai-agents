import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from agent.core import get_agent_executor
from models import Habit
from storage import get_habits, add_habit, delete_habit, log_habit, get_logs
from analytics import calculate_current_streak, calculate_completion_rate, get_best_day_of_week
from visualizations import plot_heatmap, plot_habit_progress, plot_completion_rate_trend

st.set_page_config(
    page_title="Habit Coach AI",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Feel ---
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #2c3e50;
        color: #ecf0f1;
    }
    section[data-testid="stSidebar"] h1 {
        color: #ecf0f1;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("💪 Habit Coach")

    selected_page = st.radio(
        "Navigate",
        ["Dashboard", "Coach AI", "Manage Habits"],
        index=0
    )

    st.markdown("---")
    st.markdown("### Settings")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    st.markdown("---")
    st.info("Build better habits with AI assistance.")

# --- Dashboard Page ---
if selected_page == "Dashboard":
    st.title("📊 Your Progress Dashboard")

    habits = get_habits()
    if not habits:
        st.warning("No habits found. Go to 'Manage Habits' to add one!")
    else:
        # Overview Metrics
        st.subheader("Overview")
        cols = st.columns(min(len(habits), 4))
        for i, habit in enumerate(habits[:4]):
            streak = calculate_current_streak(habit.id)
            rate = calculate_completion_rate(habit.id)
            with cols[i]:
                st.metric(label=habit.name, value=f"{streak} days", delta=f"{rate:.0f}% rate")

        st.markdown("---")

        # Detailed View
        st.subheader("Deep Dive")
        selected_habit_name = st.selectbox("Select Habit to Analyze", [h.name for h in habits])
        selected_habit = next(h for h in habits if h.name == selected_habit_name)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("#### Activity Heatmap")
            fig_heatmap = plot_heatmap(selected_habit.id)
            st.plotly_chart(fig_heatmap, use_container_width=True)

            st.markdown("#### 30-Day Progress")
            fig_progress = plot_habit_progress(selected_habit.id)
            st.plotly_chart(fig_progress, use_container_width=True)

        with col2:
            st.markdown("#### Statistics")
            streak = calculate_current_streak(selected_habit.id)
            best_day = get_best_day_of_week(selected_habit.id)
            rate = calculate_completion_rate(selected_habit.id)

            st.info(f"**Current Streak:** {streak} days")
            st.success(f"**Completion Rate:** {rate:.1f}%")
            st.warning(f"**Best Day:** {best_day}")

            st.markdown("#### Monthly Trend")
            fig_trend = plot_completion_rate_trend(selected_habit.id)
            st.plotly_chart(fig_trend, use_container_width=True)

# --- Coach AI Page ---
elif selected_page == "Coach AI":
    st.title("🤖 AI Habit Coach")
    st.markdown("Chat with your personal coach to log habits, get motivation, or analyze your data.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Habit Coach. How can I help you today? I can log your habits, add new ones, or give you a progress update."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Log a habit, ask for stats..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get AI response
        if not os.environ.get("OPENAI_API_KEY"):
            st.error("Please set your OpenAI API Key in the sidebar.")
        else:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Thinking...")

                try:
                    if "agent_executor" not in st.session_state:
                        st.session_state.agent_executor = get_agent_executor()

                    response = st.session_state.agent_executor.invoke({"input": prompt})
                    output = response["output"]

                    message_placeholder.markdown(output)
                    st.session_state.messages.append({"role": "assistant", "content": output})
                except Exception as e:
                    message_placeholder.error(f"Error: {str(e)}")

# --- Manage Habits Page ---
elif selected_page == "Manage Habits":
    st.title("🛠️ Manage Habits")

    tab1, tab2 = st.tabs(["Add / Edit Habits", "Manual Log"])

    with tab1:
        st.subheader("Add New Habit")
        with st.form("add_habit_form"):
            name = st.text_input("Habit Name", placeholder="e.g., Morning Jog")
            desc = st.text_area("Description", placeholder="Run 5km every morning")
            freq = st.selectbox("Frequency", ["daily", "weekly"])
            submitted = st.form_submit_button("Add Habit")

            if submitted and name:
                add_habit(name, desc, freq)
                st.success(f"Added habit: {name}")
                st.rerun()

        st.markdown("---")
        st.subheader("Your Habits")
        habits = get_habits()
        for h in habits:
            col1, col2, col3 = st.columns([3, 2, 1])
            col1.markdown(f"**{h.name}**")
            col2.markdown(f"_{h.frequency}_")
            if col3.button("Delete", key=f"del_{h.id}"):
                delete_habit(h.id)
                st.rerun()

    with tab2:
        st.subheader("Log Past Activity")
        habits = get_habits()
        if not habits:
            st.info("No habits to log.")
        else:
            with st.form("manual_log_form"):
                h_name = st.selectbox("Select Habit", [h.name for h in habits])
                l_date = st.date_input("Date", value=date.today())
                l_status = st.selectbox("Status", ["completed", "skipped"])
                l_notes = st.text_area("Notes")
                submitted = st.form_submit_button("Log Activity")

                if submitted:
                    h_obj = next(h for h in habits if h.name == h_name)
                    log_habit(h_obj.id, l_date, l_status, l_notes)
                    st.success(f"Logged {h_name} for {l_date}")
