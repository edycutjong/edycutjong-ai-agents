import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover
import tempfile  # pragma: no cover
import time  # pragma: no cover

# Ensure local imports work
current_dir = os.path.dirname(os.path.abspath(__file__))  # pragma: no cover
if current_dir not in sys.path:  # pragma: no cover
    sys.path.insert(0, current_dir)  # pragma: no cover

try:  # pragma: no cover
    from config import Config  # pragma: no cover
    from agent.utils import extract_audio  # pragma: no cover
    from agent.transcriber import Transcriber  # pragma: no cover
    from agent.analysis import ContentAnalyzer  # pragma: no cover
except ImportError as e:  # pragma: no cover
    st.error(f"Import Error: {e}. Please run streamlit from the app directory.")  # pragma: no cover
    st.stop()  # pragma: no cover

# --- UI Config ---
st.set_page_config(  # pragma: no cover
    page_title="Video to Transcript Agent",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""  # pragma: no cover
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
with st.sidebar:  # pragma: no cover
    st.title("Settings")  # pragma: no cover

    api_key = st.text_input("OpenAI API Key", type="password", value=Config.OPENAI_API_KEY or "")  # pragma: no cover
    if not api_key:  # pragma: no cover
        st.warning("Please enter your OpenAI API Key to proceed.")  # pragma: no cover

    language = st.text_input("Language Code (e.g. 'en', 'fr')", help="Leave empty for auto-detect")  # pragma: no cover

    st.divider()  # pragma: no cover

    st.subheader("Analysis")  # pragma: no cover
    enable_analysis = st.checkbox("Generate Summary & Chapters", value=True)  # pragma: no cover

    st.divider()  # pragma: no cover
    st.caption("Powered by OpenAI Whisper & LangChain")  # pragma: no cover

# --- Main Content ---
st.markdown("<h1 class='main-header'>🎬 Video to Transcript Agent</h1>", unsafe_allow_html=True)  # pragma: no cover
st.markdown("Upload a video or audio file to generate a transcript, summary, and chapter markers.", unsafe_allow_html=True)  # pragma: no cover

uploaded_file = st.file_uploader("Choose a file", type=['mp4', 'mov', 'avi', 'mp3', 'wav', 'm4a', 'flac', 'webm'])  # pragma: no cover

if uploaded_file is not None and api_key:  # pragma: no cover
    st.info(f"File uploaded: {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.2f} MB)")  # pragma: no cover

    if st.button("Start Processing"):  # pragma: no cover
        # Save uploaded file to temp
        suffix = os.path.splitext(uploaded_file.name)[1]  # pragma: no cover
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=Config.TEMP_DIR) as tmp_file:  # pragma: no cover
            tmp_file.write(uploaded_file.getvalue())  # pragma: no cover
            input_path = tmp_file.name  # pragma: no cover

        status_text = st.empty()  # pragma: no cover
        progress_bar = st.progress(0)  # pragma: no cover

        try:  # pragma: no cover
            # 1. Extract Audio
            status_text.text("Extracting audio...")  # pragma: no cover
            temp_audio_path = os.path.join(Config.TEMP_DIR, f"temp_{int(time.time())}.mp3")  # pragma: no cover
            audio_path = extract_audio(input_path, temp_audio_path)  # pragma: no cover
            progress_bar.progress(30)  # pragma: no cover

            # 2. Transcribe
            status_text.text("Transcribing (this may take a while)...")  # pragma: no cover
            transcriber = Transcriber(api_key=api_key)  # pragma: no cover
            transcript_text = transcriber.transcribe(audio_path, response_format="text", language=language or None)  # pragma: no cover

            progress_bar.progress(70)  # pragma: no cover

            # 3. Analyze
            summary = ""  # pragma: no cover
            chapters = ""  # pragma: no cover
            if enable_analysis:  # pragma: no cover
                status_text.text("Analyzing content...")  # pragma: no cover
                try:  # pragma: no cover
                    analyzer = ContentAnalyzer(api_key=api_key)  # pragma: no cover
                    summary = analyzer.summarize(transcript_text)  # pragma: no cover
                    chapters = analyzer.generate_chapters(transcript_text)  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.warning(f"Analysis failed: {e}")  # pragma: no cover
                    summary = "Analysis failed."  # pragma: no cover
                    chapters = "Analysis failed."  # pragma: no cover

            progress_bar.progress(100)  # pragma: no cover
            status_text.text("Done!")  # pragma: no cover

            # --- Display Results ---
            tab1, tab2, tab3 = st.tabs(["Transcript", "Summary", "Chapters"])  # pragma: no cover

            with tab1:  # pragma: no cover
                st.text_area("Full Transcript", transcript_text, height=400)  # pragma: no cover
                st.download_button("Download Transcript (.txt)", transcript_text, file_name=f"{uploaded_file.name}_transcript.txt")  # pragma: no cover

            with tab2:  # pragma: no cover
                if enable_analysis:  # pragma: no cover
                    st.markdown(summary)  # pragma: no cover
                    st.download_button("Download Summary (.md)", summary, file_name=f"{uploaded_file.name}_summary.md")  # pragma: no cover
                else:
                    st.info("Analysis disabled.")  # pragma: no cover

            with tab3:  # pragma: no cover
                if enable_analysis:  # pragma: no cover
                    st.markdown(chapters)  # pragma: no cover
                    st.download_button("Download Chapters (.md)", chapters, file_name=f"{uploaded_file.name}_chapters.md")  # pragma: no cover
                else:
                    st.info("Analysis disabled.")  # pragma: no cover

            # Cleanup (optional, maybe keep for debug or if tempfile handles it)
            # os.unlink(input_path) # tempfile usually deletes if delete=True, but we set False.
            # We should probably clean up
            try:  # pragma: no cover
                os.unlink(input_path)  # pragma: no cover
                if os.path.exists(temp_audio_path) and temp_audio_path != input_path:  # pragma: no cover
                    os.unlink(temp_audio_path)  # pragma: no cover
            except:  # pragma: no cover
                pass  # pragma: no cover

        except Exception as e:  # pragma: no cover
            st.error(f"An error occurred: {str(e)}")  # pragma: no cover
            progress_bar.empty()  # pragma: no cover

elif not api_key:  # pragma: no cover
    st.info("Please enter your OpenAI API Key in the sidebar to start.")  # pragma: no cover
