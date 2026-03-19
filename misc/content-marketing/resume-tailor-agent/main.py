import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover
import datetime  # pragma: no cover

# Ensure the root directory is in sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover

from agent.core import ResumeTailorAgent  # pragma: no cover
from agent.utils import read_pdf, create_pdf  # pragma: no cover
from config import Config  # pragma: no cover

# --- PAGE CONFIGURATION ---
st.set_page_config(  # pragma: no cover
    page_title="Resume Tailor Agent",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM UI ---
st.markdown("""  # pragma: no cover
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
with st.sidebar:  # pragma: no cover
    st.image("https://img.icons8.com/color/96/000000/resume.png", width=80)  # pragma: no cover
    st.title("Settings")  # pragma: no cover

    api_key_input = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY") or "")  # pragma: no cover
    if api_key_input:  # pragma: no cover
        Config.OPENAI_API_KEY = api_key_input  # pragma: no cover

    model_name = st.selectbox("Model", ["gpt-4-turbo-preview", "gpt-3.5-turbo", "gpt-4"])  # pragma: no cover
    Config.MODEL_NAME = model_name  # pragma: no cover

    st.markdown("---")  # pragma: no cover
    st.info("Upload your Master Resume and the Job Description you want to apply for. The AI will tailor your resume and write a cover letter.")  # pragma: no cover

    st.markdown("### Version Tracking")  # pragma: no cover
    if 'history' not in st.session_state:  # pragma: no cover
        st.session_state.history = []  # pragma: no cover

    for i, item in enumerate(reversed(st.session_state.history)):  # pragma: no cover
        st.caption(f"{item['timestamp']} - {item['action']}")  # pragma: no cover

# --- MAIN APP ---

st.markdown('<div class="main-header">Resume Tailor Agent</div>', unsafe_allow_html=True)  # pragma: no cover

# Initialize Agent
agent = ResumeTailorAgent()  # pragma: no cover

# Split Screen Layout
col1, col2 = st.columns(2)  # pragma: no cover

with col1:  # pragma: no cover
    st.markdown('<div class="section-header">1. Master Resume</div>', unsafe_allow_html=True)  # pragma: no cover
    resume_file = st.file_uploader("Upload PDF Resume", type=["pdf"])  # pragma: no cover
    resume_text_area = st.text_area("Or Paste Resume Text", height=300)  # pragma: no cover

    resume_content = ""  # pragma: no cover
    if resume_file:  # pragma: no cover
        resume_content = read_pdf(resume_file)  # pragma: no cover
        st.success("Resume PDF Loaded!")  # pragma: no cover
    elif resume_text_area:  # pragma: no cover
        resume_content = resume_text_area  # pragma: no cover

with col2:  # pragma: no cover
    st.markdown('<div class="section-header">2. Job Description</div>', unsafe_allow_html=True)  # pragma: no cover
    job_file = st.file_uploader("Upload Job Description (PDF/Txt)", type=["pdf", "txt"])  # pragma: no cover
    job_text_area = st.text_area("Or Paste Job Description", height=300)  # pragma: no cover

    job_description = ""  # pragma: no cover
    if job_file:  # pragma: no cover
        if job_file.type == "application/pdf":  # pragma: no cover
            job_description = read_pdf(job_file)  # pragma: no cover
        else:
            job_description = str(job_file.read(), "utf-8")  # pragma: no cover
        st.success("Job Description Loaded!")  # pragma: no cover
    elif job_text_area:  # pragma: no cover
        job_description = job_text_area  # pragma: no cover

# Action Buttons
st.markdown("---")  # pragma: no cover
action_col1, action_col2, action_col3 = st.columns([1, 1, 1])  # pragma: no cover

analyze_clicked = False  # pragma: no cover
tailor_clicked = False  # pragma: no cover
cover_letter_clicked = False  # pragma: no cover

with action_col1:  # pragma: no cover
    if st.button("🔍 Analyze Job"):  # pragma: no cover
        analyze_clicked = True  # pragma: no cover

with action_col2:  # pragma: no cover
    if st.button("✨ Tailor Resume"):  # pragma: no cover
        tailor_clicked = True  # pragma: no cover

with action_col3:  # pragma: no cover
    if st.button("✉️ Generate Cover Letter"):  # pragma: no cover
        cover_letter_clicked = True  # pragma: no cover

# --- LOGIC HANDLING ---

if analyze_clicked:  # pragma: no cover
    if not job_description:  # pragma: no cover
        st.error("Please provide a Job Description first.")  # pragma: no cover
    else:
        with st.spinner("Analyzing Job Description..."):  # pragma: no cover
            analysis = agent.analyze_job(job_description)  # pragma: no cover
            st.markdown('<div class="result-card">', unsafe_allow_html=True)  # pragma: no cover
            st.markdown("### Job Analysis")  # pragma: no cover
            st.markdown(analysis)  # pragma: no cover
            st.markdown('</div>', unsafe_allow_html=True)  # pragma: no cover
            st.session_state['job_analysis'] = analysis  # pragma: no cover

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")  # pragma: no cover
            st.session_state.history.append({"timestamp": timestamp, "action": "Analyzed Job"})  # pragma: no cover

if tailor_clicked:  # pragma: no cover
    if not resume_content or not job_description:  # pragma: no cover
        st.error("Please provide both Resume and Job Description.")  # pragma: no cover
    else:
        # Ensure analysis is done
        job_analysis = st.session_state.get('job_analysis')  # pragma: no cover
        if not job_analysis:  # pragma: no cover
            with st.spinner("Analyzing Job first..."):  # pragma: no cover
                job_analysis = agent.analyze_job(job_description)  # pragma: no cover
                st.session_state['job_analysis'] = job_analysis  # pragma: no cover

        with st.spinner("Tailoring Resume..."):  # pragma: no cover
            tailored_resume = agent.tailor_resume(resume_content, job_analysis)  # pragma: no cover
            st.session_state['tailored_resume'] = tailored_resume  # pragma: no cover

            st.markdown('<div class="result-card">', unsafe_allow_html=True)  # pragma: no cover
            st.markdown("### Tailored Resume")  # pragma: no cover
            st.markdown(tailored_resume)  # pragma: no cover
            st.markdown('</div>', unsafe_allow_html=True)  # pragma: no cover

            # PDF Export
            pdf_path = create_pdf(tailored_resume, "tailored_resume.pdf")  # pragma: no cover
            with open(pdf_path, "rb") as pdf_file:  # pragma: no cover
                st.download_button(  # pragma: no cover
                    label="Download PDF",
                    data=pdf_file,
                    file_name="tailored_resume.pdf",
                    mime="application/pdf"
                )

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")  # pragma: no cover
            st.session_state.history.append({"timestamp": timestamp, "action": "Tailored Resume"})  # pragma: no cover

if cover_letter_clicked:  # pragma: no cover
    if not resume_content or not job_description:  # pragma: no cover
        st.error("Please provide both Resume and Job Description.")  # pragma: no cover
    else:
        with st.spinner("Drafting Cover Letter..."):  # pragma: no cover
            cover_letter = agent.generate_cover_letter(resume_content, job_description)  # pragma: no cover
            st.session_state['cover_letter'] = cover_letter  # pragma: no cover

            st.markdown('<div class="result-card">', unsafe_allow_html=True)  # pragma: no cover
            st.markdown("### Cover Letter")  # pragma: no cover
            st.markdown(cover_letter)  # pragma: no cover
            st.markdown('</div>', unsafe_allow_html=True)  # pragma: no cover

            # PDF Export
            pdf_path = create_pdf(cover_letter, "cover_letter.pdf")  # pragma: no cover
            with open(pdf_path, "rb") as pdf_file:  # pragma: no cover
                st.download_button(  # pragma: no cover
                    label="Download PDF",
                    data=pdf_file,
                    file_name="cover_letter.pdf",
                    mime="application/pdf"
                )

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")  # pragma: no cover
            st.session_state.history.append({"timestamp": timestamp, "action": "Generated Cover Letter"})  # pragma: no cover
