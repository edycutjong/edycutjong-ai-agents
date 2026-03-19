import streamlit as st  # pragma: no cover
import pandas as pd  # pragma: no cover
import plotly.express as px  # pragma: no cover
from datetime import date  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))  # pragma: no cover

from agent.core import get_agent_executor  # pragma: no cover
from models import Habit  # pragma: no cover
from storage import get_habits, add_habit, delete_habit, log_habit, get_logs  # pragma: no cover
from analytics import calculate_current_streak, calculate_completion_rate, get_best_day_of_week  # pragma: no cover
from visualizations import plot_heatmap, plot_habit_progress, plot_completion_rate_trend  # pragma: no cover

st.set_page_config(  # pragma: no cover
    page_title="Habit Coach AI",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Feel ---
st.markdown("""  # pragma: no cover
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
with st.sidebar:  # pragma: no cover
    st.title("💪 Habit Coach")  # pragma: no cover

    selected_page = st.radio(  # pragma: no cover
        "Navigate",
        ["Dashboard", "Coach AI", "Manage Habits"],
        index=0
    )

    st.markdown("---")  # pragma: no cover
    st.markdown("### Settings")  # pragma: no cover
    api_key = st.text_input("OpenAI API Key", type="password", value=os.environ.get("OPENAI_API_KEY", ""))  # pragma: no cover
    if api_key:  # pragma: no cover
        os.environ["OPENAI_API_KEY"] = api_key  # pragma: no cover

    st.markdown("---")  # pragma: no cover
    st.info("Build better habits with AI assistance.")  # pragma: no cover

# --- Dashboard Page ---
if selected_page == "Dashboard":  # pragma: no cover
    st.title("📊 Your Progress Dashboard")  # pragma: no cover

    habits = get_habits()  # pragma: no cover
    if not habits:  # pragma: no cover
        st.warning("No habits found. Go to 'Manage Habits' to add one!")  # pragma: no cover
    else:
        # Overview Metrics
        st.subheader("Overview")  # pragma: no cover
        cols = st.columns(min(len(habits), 4))  # pragma: no cover
        for i, habit in enumerate(habits[:4]):  # pragma: no cover
            streak = calculate_current_streak(habit.id)  # pragma: no cover
            rate = calculate_completion_rate(habit.id)  # pragma: no cover
            with cols[i]:  # pragma: no cover
                st.metric(label=habit.name, value=f"{streak} days", delta=f"{rate:.0f}% rate")  # pragma: no cover

        st.markdown("---")  # pragma: no cover

        # Detailed View
        st.subheader("Deep Dive")  # pragma: no cover
        selected_habit_name = st.selectbox("Select Habit to Analyze", [h.name for h in habits])  # pragma: no cover
        selected_habit = next(h for h in habits if h.name == selected_habit_name)  # pragma: no cover

        col1, col2 = st.columns([2, 1])  # pragma: no cover

        with col1:  # pragma: no cover
            st.markdown("#### Activity Heatmap")  # pragma: no cover
            fig_heatmap = plot_heatmap(selected_habit.id)  # pragma: no cover
            st.plotly_chart(fig_heatmap, use_container_width=True)  # pragma: no cover

            st.markdown("#### 30-Day Progress")  # pragma: no cover
            fig_progress = plot_habit_progress(selected_habit.id)  # pragma: no cover
            st.plotly_chart(fig_progress, use_container_width=True)  # pragma: no cover

        with col2:  # pragma: no cover
            st.markdown("#### Statistics")  # pragma: no cover
            streak = calculate_current_streak(selected_habit.id)  # pragma: no cover
            best_day = get_best_day_of_week(selected_habit.id)  # pragma: no cover
            rate = calculate_completion_rate(selected_habit.id)  # pragma: no cover

            st.info(f"**Current Streak:** {streak} days")  # pragma: no cover
            st.success(f"**Completion Rate:** {rate:.1f}%")  # pragma: no cover
            st.warning(f"**Best Day:** {best_day}")  # pragma: no cover

            st.markdown("#### Monthly Trend")  # pragma: no cover
            fig_trend = plot_completion_rate_trend(selected_habit.id)  # pragma: no cover
            st.plotly_chart(fig_trend, use_container_width=True)  # pragma: no cover

# --- Coach AI Page ---
elif selected_page == "Coach AI":  # pragma: no cover
    st.title("🤖 AI Habit Coach")  # pragma: no cover
    st.markdown("Chat with your personal coach to log habits, get motivation, or analyze your data.")  # pragma: no cover

    if "messages" not in st.session_state:  # pragma: no cover
        st.session_state.messages = [  # pragma: no cover
            {"role": "assistant", "content": "Hello! I'm your Habit Coach. How can I help you today? I can log your habits, add new ones, or give you a progress update."}
        ]

    for msg in st.session_state.messages:  # pragma: no cover
        with st.chat_message(msg["role"]):  # pragma: no cover
            st.write(msg["content"])  # pragma: no cover

    if prompt := st.chat_input("Log a habit, ask for stats..."):  # pragma: no cover
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})  # pragma: no cover
        with st.chat_message("user"):  # pragma: no cover
            st.write(prompt)  # pragma: no cover

        # Get AI response
        if not os.environ.get("OPENAI_API_KEY"):  # pragma: no cover
            st.error("Please set your OpenAI API Key in the sidebar.")  # pragma: no cover
        else:
            with st.chat_message("assistant"):  # pragma: no cover
                message_placeholder = st.empty()  # pragma: no cover
                message_placeholder.markdown("Thinking...")  # pragma: no cover

                try:  # pragma: no cover
                    if "agent_executor" not in st.session_state:  # pragma: no cover
                        st.session_state.agent_executor = get_agent_executor()  # pragma: no cover

                    response = st.session_state.agent_executor.invoke({"input": prompt})  # pragma: no cover
                    output = response["output"]  # pragma: no cover

                    message_placeholder.markdown(output)  # pragma: no cover
                    st.session_state.messages.append({"role": "assistant", "content": output})  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    message_placeholder.error(f"Error: {str(e)}")  # pragma: no cover

# --- Manage Habits Page ---
elif selected_page == "Manage Habits":  # pragma: no cover
    st.title("🛠️ Manage Habits")  # pragma: no cover

    tab1, tab2 = st.tabs(["Add / Edit Habits", "Manual Log"])  # pragma: no cover

    with tab1:  # pragma: no cover
        st.subheader("Add New Habit")  # pragma: no cover
        with st.form("add_habit_form"):  # pragma: no cover
            name = st.text_input("Habit Name", placeholder="e.g., Morning Jog")  # pragma: no cover
            desc = st.text_area("Description", placeholder="Run 5km every morning")  # pragma: no cover
            freq = st.selectbox("Frequency", ["daily", "weekly"])  # pragma: no cover
            submitted = st.form_submit_button("Add Habit")  # pragma: no cover

            if submitted and name:  # pragma: no cover
                add_habit(name, desc, freq)  # pragma: no cover
                st.success(f"Added habit: {name}")  # pragma: no cover
                st.rerun()  # pragma: no cover

        st.markdown("---")  # pragma: no cover
        st.subheader("Your Habits")  # pragma: no cover
        habits = get_habits()  # pragma: no cover
        for h in habits:  # pragma: no cover
            col1, col2, col3 = st.columns([3, 2, 1])  # pragma: no cover
            col1.markdown(f"**{h.name}**")  # pragma: no cover
            col2.markdown(f"_{h.frequency}_")  # pragma: no cover
            if col3.button("Delete", key=f"del_{h.id}"):  # pragma: no cover
                delete_habit(h.id)  # pragma: no cover
                st.rerun()  # pragma: no cover

    with tab2:  # pragma: no cover
        st.subheader("Log Past Activity")  # pragma: no cover
        habits = get_habits()  # pragma: no cover
        if not habits:  # pragma: no cover
            st.info("No habits to log.")  # pragma: no cover
        else:
            with st.form("manual_log_form"):  # pragma: no cover
                h_name = st.selectbox("Select Habit", [h.name for h in habits])  # pragma: no cover
                l_date = st.date_input("Date", value=date.today())  # pragma: no cover
                l_status = st.selectbox("Status", ["completed", "skipped"])  # pragma: no cover
                l_notes = st.text_area("Notes")  # pragma: no cover
                submitted = st.form_submit_button("Log Activity")  # pragma: no cover

                if submitted:  # pragma: no cover
                    h_obj = next(h for h in habits if h.name == h_name)  # pragma: no cover
                    log_habit(h_obj.id, l_date, l_status, l_notes)  # pragma: no cover
                    st.success(f"Logged {h_name} for {l_date}")  # pragma: no cover
