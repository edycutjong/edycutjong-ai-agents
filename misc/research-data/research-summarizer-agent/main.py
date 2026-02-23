import streamlit as st
import os
import time
from datetime import datetime
from config import Config
from agent.researcher import ResearchAgent
from utils.pdf_generator import generate_pdf

# Page config
st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
        color: #E0E7FF;
    }

    h1, h2, h3 {
        color: #C7D2FE !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #6366F1 0%, #818CF8 100%);
        border: none;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }

    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid #4F46E5;
    }

    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid #4F46E5;
    }

    div[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }

    div[data-testid="stStatusWidget"] {
        background-color: rgba(30, 27, 75, 0.8);
        border: 1px solid #4F46E5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "research_running" not in st.session_state:
    st.session_state.research_running = False
if "final_report" not in st.session_state:
    st.session_state.final_report = None
if "current_status" not in st.session_state:
    st.session_state.current_status = ""

# Sidebar: History & Settings
with st.sidebar:
    st.title("Research History")

    # Load history
    if os.path.exists(Config.HISTORY_DIR):
        files = sorted(os.listdir(Config.HISTORY_DIR), reverse=True)
        for file in files:
            if file.endswith(".md"):
                if st.button(file.replace(".md", ""), key=file):
                    with open(os.path.join(Config.HISTORY_DIR, file), "r") as f:
                        st.session_state.final_report = f.read()
                        st.rerun()
    else:
        st.write("No history found.")

    st.divider()
    st.write("Created by Jules")

# Main content
st.title("🔍 Deep Research Agent")
st.markdown("Enter a topic below to start a comprehensive research process.")

col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_input("Research Topic", placeholder="e.g., The Future of Quantum Computing")

with col2:
    depth = st.selectbox("Research Depth", ["Overview", "Deep Dive", "Comprehensive"], index=1)

domains = st.multiselect(
    "Focus Domains",
    ["Technology", "Science", "Business", "History", "Health", "Politics", "Environment"],
    default=["Technology", "Science"]
)

start_button = st.button("Start Research", type="primary", disabled=st.session_state.research_running)

if start_button and topic:
    st.session_state.research_running = True
    st.session_state.final_report = None

    agent = ResearchAgent()

    with st.status("Researching...", expanded=True) as status:
        def update_ui(msg):
            status.write(msg)

        final_report = agent.run_research(topic, depth, domains, status_callback=update_ui)
        status.update(label="Research Complete!", state="complete", expanded=False)

    st.session_state.final_report = final_report
    st.session_state.research_running = False

    # Save to history
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{topic.replace(' ', '_')}_{timestamp}.md"
    filepath = os.path.join(Config.HISTORY_DIR, filename)
    with open(filepath, "w") as f:
        f.write(final_report)

    st.rerun()
elif start_button and not topic:
    st.error("Please enter a research topic.")

# Placeholder for results
status_container = st.empty()
report_container = st.container()

if st.session_state.final_report:
    with report_container:
        st.markdown("## Final Report")
        st.markdown(st.session_state.final_report)

        # Download buttons
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        st.download_button(
            label="Download Markdown",
            data=st.session_state.final_report,
            file_name=f"research_report_{timestamp}.md",
            mime="text/markdown"
        )

        # Generate PDF on the fly
        # We need a temporary file or bytes buffer. reportlab writes to file.
        # We can use a temp file.
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
            generate_pdf(st.session_state.final_report, tmp_pdf.name)
            with open(tmp_pdf.name, "rb") as f:
                pdf_data = f.read()
            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name=f"research_report_{timestamp}.pdf",
                mime="application/pdf"
            )
