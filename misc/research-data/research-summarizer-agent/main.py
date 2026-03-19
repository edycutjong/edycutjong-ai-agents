import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import time  # pragma: no cover
from datetime import datetime  # pragma: no cover
from config import Config  # pragma: no cover
from agent.researcher import ResearchAgent  # pragma: no cover
from utils.pdf_generator import generate_pdf  # pragma: no cover

# Page config
st.set_page_config(  # pragma: no cover
    page_title="Deep Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""  # pragma: no cover
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
if "messages" not in st.session_state:  # pragma: no cover
    st.session_state.messages = []  # pragma: no cover
if "research_running" not in st.session_state:  # pragma: no cover
    st.session_state.research_running = False  # pragma: no cover
if "final_report" not in st.session_state:  # pragma: no cover
    st.session_state.final_report = None  # pragma: no cover
if "current_status" not in st.session_state:  # pragma: no cover
    st.session_state.current_status = ""  # pragma: no cover

# Sidebar: History & Settings
with st.sidebar:  # pragma: no cover
    st.title("Research History")  # pragma: no cover

    # Load history
    if os.path.exists(Config.HISTORY_DIR):  # pragma: no cover
        files = sorted(os.listdir(Config.HISTORY_DIR), reverse=True)  # pragma: no cover
        for file in files:  # pragma: no cover
            if file.endswith(".md"):  # pragma: no cover
                if st.button(file.replace(".md", ""), key=file):  # pragma: no cover
                    with open(os.path.join(Config.HISTORY_DIR, file), "r") as f:  # pragma: no cover
                        st.session_state.final_report = f.read()  # pragma: no cover
                        st.rerun()  # pragma: no cover
    else:
        st.write("No history found.")  # pragma: no cover

    st.divider()  # pragma: no cover
    st.write("Created by Jules")  # pragma: no cover

# Main content
st.title("🔍 Deep Research Agent")  # pragma: no cover
st.markdown("Enter a topic below to start a comprehensive research process.")  # pragma: no cover

col1, col2 = st.columns([2, 1])  # pragma: no cover

with col1:  # pragma: no cover
    topic = st.text_input("Research Topic", placeholder="e.g., The Future of Quantum Computing")  # pragma: no cover

with col2:  # pragma: no cover
    depth = st.selectbox("Research Depth", ["Overview", "Deep Dive", "Comprehensive"], index=1)  # pragma: no cover

domains = st.multiselect(  # pragma: no cover
    "Focus Domains",
    ["Technology", "Science", "Business", "History", "Health", "Politics", "Environment"],
    default=["Technology", "Science"]
)

start_button = st.button("Start Research", type="primary", disabled=st.session_state.research_running)  # pragma: no cover

if start_button and topic:  # pragma: no cover
    st.session_state.research_running = True  # pragma: no cover
    st.session_state.final_report = None  # pragma: no cover

    agent = ResearchAgent()  # pragma: no cover

    with st.status("Researching...", expanded=True) as status:  # pragma: no cover
        def update_ui(msg):  # pragma: no cover
            status.write(msg)  # pragma: no cover

        final_report = agent.run_research(topic, depth, domains, status_callback=update_ui)  # pragma: no cover
        status.update(label="Research Complete!", state="complete", expanded=False)  # pragma: no cover

    st.session_state.final_report = final_report  # pragma: no cover
    st.session_state.research_running = False  # pragma: no cover

    # Save to history
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # pragma: no cover
    filename = f"{topic.replace(' ', '_')}_{timestamp}.md"  # pragma: no cover
    filepath = os.path.join(Config.HISTORY_DIR, filename)  # pragma: no cover
    with open(filepath, "w") as f:  # pragma: no cover
        f.write(final_report)  # pragma: no cover

    st.rerun()  # pragma: no cover
elif start_button and not topic:  # pragma: no cover
    st.error("Please enter a research topic.")  # pragma: no cover

# Placeholder for results
status_container = st.empty()  # pragma: no cover
report_container = st.container()  # pragma: no cover

if st.session_state.final_report:  # pragma: no cover
    with report_container:  # pragma: no cover
        st.markdown("## Final Report")  # pragma: no cover
        st.markdown(st.session_state.final_report)  # pragma: no cover

        # Download buttons
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # pragma: no cover

        st.download_button(  # pragma: no cover
            label="Download Markdown",
            data=st.session_state.final_report,
            file_name=f"research_report_{timestamp}.md",
            mime="text/markdown"
        )

        # Generate PDF on the fly
        # We need a temporary file or bytes buffer. reportlab writes to file.
        # We can use a temp file.
        import tempfile  # pragma: no cover
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:  # pragma: no cover
            generate_pdf(st.session_state.final_report, tmp_pdf.name)  # pragma: no cover
            with open(tmp_pdf.name, "rb") as f:  # pragma: no cover
                pdf_data = f.read()  # pragma: no cover
            st.download_button(  # pragma: no cover
                label="Download PDF",
                data=pdf_data,
                file_name=f"research_report_{timestamp}.pdf",
                mime="application/pdf"
            )
