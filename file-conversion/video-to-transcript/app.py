import streamlit as st
import os
import sys
import tempfile
import time

# Ensure local imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from config import Config
    from agent.utils import extract_audio
    from agent.transcriber import Transcriber
    from agent.analysis import ContentAnalyzer
except ImportError as e:
    st.error(f"Import Error: {e}. Please run streamlit from the app directory.")
    st.stop()

# --- UI Config ---
st.set_page_config(
    page_title="Video to Transcript Agent",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #FF2B2B;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("Settings")

    api_key = st.text_input("OpenAI API Key", type="password", value=Config.OPENAI_API_KEY or "")
    if not api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")

    language = st.text_input("Language Code (e.g. 'en', 'fr')", help="Leave empty for auto-detect")

    st.divider()

    st.subheader("Analysis")
    enable_analysis = st.checkbox("Generate Summary & Chapters", value=True)

    st.divider()
    st.caption("Powered by OpenAI Whisper & LangChain")

# --- Main Content ---
st.markdown("<h1 class='main-header'>🎬 Video to Transcript Agent</h1>", unsafe_allow_html=True)
st.markdown("Upload a video or audio file to generate a transcript, summary, and chapter markers.", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file", type=['mp4', 'mov', 'avi', 'mp3', 'wav', 'm4a', 'flac', 'webm'])

if uploaded_file is not None and api_key:
    st.info(f"File uploaded: {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.2f} MB)")

    if st.button("Start Processing"):
        # Save uploaded file to temp
        suffix = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=Config.TEMP_DIR) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            input_path = tmp_file.name

        status_text = st.empty()
        progress_bar = st.progress(0)

        try:
            # 1. Extract Audio
            status_text.text("Extracting audio...")
            temp_audio_path = os.path.join(Config.TEMP_DIR, f"temp_{int(time.time())}.mp3")
            audio_path = extract_audio(input_path, temp_audio_path)
            progress_bar.progress(30)

            # 2. Transcribe
            status_text.text("Transcribing (this may take a while)...")
            transcriber = Transcriber(api_key=api_key)
            transcript_text = transcriber.transcribe(audio_path, response_format="text", language=language or None)

            progress_bar.progress(70)

            # 3. Analyze
            summary = ""
            chapters = ""
            if enable_analysis:
                status_text.text("Analyzing content...")
                try:
                    analyzer = ContentAnalyzer(api_key=api_key)
                    summary = analyzer.summarize(transcript_text)
                    chapters = analyzer.generate_chapters(transcript_text)
                except Exception as e:
                    st.warning(f"Analysis failed: {e}")
                    summary = "Analysis failed."
                    chapters = "Analysis failed."

            progress_bar.progress(100)
            status_text.text("Done!")

            # --- Display Results ---
            tab1, tab2, tab3 = st.tabs(["Transcript", "Summary", "Chapters"])

            with tab1:
                st.text_area("Full Transcript", transcript_text, height=400)
                st.download_button("Download Transcript (.txt)", transcript_text, file_name=f"{uploaded_file.name}_transcript.txt")

            with tab2:
                if enable_analysis:
                    st.markdown(summary)
                    st.download_button("Download Summary (.md)", summary, file_name=f"{uploaded_file.name}_summary.md")
                else:
                    st.info("Analysis disabled.")

            with tab3:
                if enable_analysis:
                    st.markdown(chapters)
                    st.download_button("Download Chapters (.md)", chapters, file_name=f"{uploaded_file.name}_chapters.md")
                else:
                    st.info("Analysis disabled.")

            # Cleanup (optional, maybe keep for debug or if tempfile handles it)
            # os.unlink(input_path) # tempfile usually deletes if delete=True, but we set False.
            # We should probably clean up
            try:
                os.unlink(input_path)
                if os.path.exists(temp_audio_path) and temp_audio_path != input_path:
                    os.unlink(temp_audio_path)
            except:
                pass

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            progress_bar.empty()

elif not api_key:
    st.info("Please enter your OpenAI API Key in the sidebar to start.")
