import streamlit as st
import os
import sys
import datetime

# Ensure the root directory is in sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.core import ResumeTailorAgent
from agent.utils import read_pdf, create_pdf
from config import Config

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Resume Tailor Agent",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a8a; /* Dark Blue */
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    .stButton>button {
        background: linear-gradient(to right, #2563eb, #3b82f6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .stButton>button:hover {
        background: linear-gradient(to right, #1d4ed8, #2563eb);
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .stTextArea>div>div>textarea {
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.05);
    }

    .stFileUploader>div>div>button {
        background-color: #ffffff;
        color: #374151;
        border: 1px solid #d1d5db;
    }

    /* Card-like containers for results */
    .result-card {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/resume.png", width=80)
    st.title("Settings")

    api_key_input = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY") or "")
    if api_key_input:
        Config.OPENAI_API_KEY = api_key_input

    model_name = st.selectbox("Model", ["gpt-4-turbo-preview", "gpt-3.5-turbo", "gpt-4"])
    Config.MODEL_NAME = model_name

    st.markdown("---")
    st.info("Upload your Master Resume and the Job Description you want to apply for. The AI will tailor your resume and write a cover letter.")

    st.markdown("### Version Tracking")
    if 'history' not in st.session_state:
        st.session_state.history = []

    for i, item in enumerate(reversed(st.session_state.history)):
        st.caption(f"{item['timestamp']} - {item['action']}")

# --- MAIN APP ---

st.markdown('<div class="main-header">Resume Tailor Agent</div>', unsafe_allow_html=True)

# Initialize Agent
agent = ResumeTailorAgent()

# Split Screen Layout
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header">1. Master Resume</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    resume_text_area = st.text_area("Or Paste Resume Text", height=300)

    resume_content = ""
    if resume_file:
        resume_content = read_pdf(resume_file)
        st.success("Resume PDF Loaded!")
    elif resume_text_area:
        resume_content = resume_text_area

with col2:
    st.markdown('<div class="section-header">2. Job Description</div>', unsafe_allow_html=True)
    job_file = st.file_uploader("Upload Job Description (PDF/Txt)", type=["pdf", "txt"])
    job_text_area = st.text_area("Or Paste Job Description", height=300)

    job_description = ""
    if job_file:
        if job_file.type == "application/pdf":
            job_description = read_pdf(job_file)
        else:
            job_description = str(job_file.read(), "utf-8")
        st.success("Job Description Loaded!")
    elif job_text_area:
        job_description = job_text_area

# Action Buttons
st.markdown("---")
action_col1, action_col2, action_col3 = st.columns([1, 1, 1])

analyze_clicked = False
tailor_clicked = False
cover_letter_clicked = False

with action_col1:
    if st.button("🔍 Analyze Job"):
        analyze_clicked = True

with action_col2:
    if st.button("✨ Tailor Resume"):
        tailor_clicked = True

with action_col3:
    if st.button("✉️ Generate Cover Letter"):
        cover_letter_clicked = True

# --- LOGIC HANDLING ---

if analyze_clicked:
    if not job_description:
        st.error("Please provide a Job Description first.")
    else:
        with st.spinner("Analyzing Job Description..."):
            analysis = agent.analyze_job(job_description)
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("### Job Analysis")
            st.markdown(analysis)
            st.markdown('</div>', unsafe_allow_html=True)
            st.session_state['job_analysis'] = analysis

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.history.append({"timestamp": timestamp, "action": "Analyzed Job"})

if tailor_clicked:
    if not resume_content or not job_description:
        st.error("Please provide both Resume and Job Description.")
    else:
        # Ensure analysis is done
        job_analysis = st.session_state.get('job_analysis')
        if not job_analysis:
            with st.spinner("Analyzing Job first..."):
                job_analysis = agent.analyze_job(job_description)
                st.session_state['job_analysis'] = job_analysis

        with st.spinner("Tailoring Resume..."):
            tailored_resume = agent.tailor_resume(resume_content, job_analysis)
            st.session_state['tailored_resume'] = tailored_resume

            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("### Tailored Resume")
            st.markdown(tailored_resume)
            st.markdown('</div>', unsafe_allow_html=True)

            # PDF Export
            pdf_path = create_pdf(tailored_resume, "tailored_resume.pdf")
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="tailored_resume.pdf",
                    mime="application/pdf"
                )

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.history.append({"timestamp": timestamp, "action": "Tailored Resume"})

if cover_letter_clicked:
    if not resume_content or not job_description:
        st.error("Please provide both Resume and Job Description.")
    else:
        with st.spinner("Drafting Cover Letter..."):
            cover_letter = agent.generate_cover_letter(resume_content, job_description)
            st.session_state['cover_letter'] = cover_letter

            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("### Cover Letter")
            st.markdown(cover_letter)
            st.markdown('</div>', unsafe_allow_html=True)

            # PDF Export
            pdf_path = create_pdf(cover_letter, "cover_letter.pdf")
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="cover_letter.pdf",
                    mime="application/pdf"
                )

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.history.append({"timestamp": timestamp, "action": "Generated Cover Letter"})
