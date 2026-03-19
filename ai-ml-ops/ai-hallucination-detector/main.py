import streamlit as st  # pragma: no cover
import tempfile  # pragma: no cover
import os  # pragma: no cover
import shutil  # pragma: no cover

# Add the current directory to sys.path to allow imports
import sys  # pragma: no cover
sys.path.append(os.path.dirname(__file__))  # pragma: no cover

from agent.detector import HallucinationDetector  # pragma: no cover

st.set_page_config(  # pragma: no cover
    page_title="AI Hallucination Detector",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS for Premium UI ---
st.markdown("""  # pragma: no cover
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .report-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .claim-verified {
        border-left: 5px solid #4CAF50;
        padding-left: 10px;
        margin-bottom: 10px;
    }
    .claim-hallucination {
        border-left: 5px solid #F44336;
        padding-left: 10px;
        margin-bottom: 10px;
    }
    .claim-unsupported {
        border-left: 5px solid #FFC107;
        padding-left: 10px;
        margin-bottom: 10px;
    }
    h1, h2, h3 {
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:  # pragma: no cover
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620536.png", width=100) # Placeholder icon  # pragma: no cover
    st.title("Settings")  # pragma: no cover

    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API Key if not set in .env")  # pragma: no cover
    if api_key:  # pragma: no cover
        os.environ["OPENAI_API_KEY"] = api_key  # pragma: no cover

    st.markdown("---")  # pragma: no cover
    st.markdown("### How it works")  # pragma: no cover
    st.markdown("1. Upload a **Source Document** (PDF or TXT).")  # pragma: no cover
    st.markdown("2. Paste the **AI Generated Text** you want to verify.")  # pragma: no cover
    st.markdown("3. Click **Analyze** to detect hallucinations.")  # pragma: no cover

    st.markdown("---")  # pragma: no cover
    st.info("Built with LangChain & Streamlit")  # pragma: no cover

# --- Main Content ---
st.title("🕵️ AI Hallucination Detector")  # pragma: no cover
st.markdown("### Verify AI outputs against source documents with confidence.")  # pragma: no cover

col1, col2 = st.columns([1, 1])  # pragma: no cover

with col1:  # pragma: no cover
    st.subheader("1. Source Document")  # pragma: no cover
    uploaded_file = st.file_uploader("Upload reference document", type=["pdf", "txt"])  # pragma: no cover

with col2:  # pragma: no cover
    st.subheader("2. AI Output")  # pragma: no cover
    ai_text = st.text_area("Paste the text to verify here", height=200, placeholder="The generated summary or content...")  # pragma: no cover

if st.button("Analyze Content"):  # pragma: no cover
    if not uploaded_file or not ai_text:  # pragma: no cover
        st.error("Please upload a source document and provide AI text.")  # pragma: no cover
    elif not os.environ.get("OPENAI_API_KEY"):  # pragma: no cover
        st.error("Please provide an OpenAI API Key.")  # pragma: no cover
    else:
        with st.spinner("Analyzing claims and verifying against source..."):  # pragma: no cover
            try:  # pragma: no cover
                # Save uploaded file to temp
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:  # pragma: no cover
                    shutil.copyfileobj(uploaded_file, tmp_file)  # pragma: no cover
                    tmp_path = tmp_file.name  # pragma: no cover

                # Initialize Detector
                detector = HallucinationDetector()  # pragma: no cover

                # Run Analysis
                # We need to adapt the method signature if I changed it.
                # I defined process(ai_text, source_file_path)

                # First, process document into vector store
                vectorstore = detector.process_document(tmp_path)  # pragma: no cover

                # Extract claims
                claims = detector.extract_claims(ai_text)  # pragma: no cover

                results = []  # pragma: no cover
                verified_count = 0  # pragma: no cover

                progress_bar = st.progress(0)  # pragma: no cover
                status_text = st.empty()  # pragma: no cover

                total_claims = len(claims)  # pragma: no cover

                for i, claim in enumerate(claims):  # pragma: no cover
                    status_text.text(f"Verifying claim {i+1}/{total_claims}...")  # pragma: no cover
                    verification = detector.verify_claim(claim, vectorstore)  # pragma: no cover
                    results.append(verification)  # pragma: no cover

                    if verification.get("status") == "VERIFIED":  # pragma: no cover
                        verified_count += 1  # pragma: no cover

                    progress_bar.progress((i + 1) / total_claims)  # pragma: no cover

                status_text.empty()  # pragma: no cover
                progress_bar.empty()  # pragma: no cover

                # Calculate Score
                score = (verified_count / total_claims) * 100 if total_claims > 0 else 0  # pragma: no cover

                # --- Display Results ---
                st.markdown("---")  # pragma: no cover
                st.subheader("Analysis Report")  # pragma: no cover

                # Score Card
                score_color = "green" if score > 80 else "orange" if score > 50 else "red"  # pragma: no cover
                st.markdown(f"""  # pragma: no cover
                <div style="text-align: center; padding: 20px; background-color: #fff; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3>Trust Score</h3>
                    <h1 style="color: {score_color}; font-size: 4rem; margin: 0;">{score:.1f}%</h1>
                    <p>{verified_count} of {total_claims} claims verified</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)  # pragma: no cover

                # Detailed Claims
                st.subheader("Detailed Claim Analysis")  # pragma: no cover

                for res in results:  # pragma: no cover
                    status = res.get("status", "UNKNOWN")  # pragma: no cover
                    confidence = res.get("confidence", 0.0)  # pragma: no cover
                    claim_text = res.get("claim", "")  # pragma: no cover
                    explanation = res.get("explanation", "")  # pragma: no cover

                    icon = "✅" if status == "VERIFIED" else "❌" if status == "HALLUCINATION" or status == "CONTRADICTED" else "⚠️"  # pragma: no cover
                    css_class = "claim-verified" if status == "VERIFIED" else "claim-hallucination" if status == "HALLUCINATION" or status == "CONTRADICTED" else "claim-unsupported"  # pragma: no cover

                    with st.expander(f"{icon} {claim_text[:80]}..."):  # pragma: no cover
                        st.markdown(f"""  # pragma: no cover
                        <div class="{css_class}">
                            <strong>Status:</strong> {status}<br>
                            <strong>Confidence:</strong> {confidence}<br>
                            <strong>Claim:</strong> {claim_text}
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"**Explanation:** {explanation}")  # pragma: no cover

                        if res.get("sources"):  # pragma: no cover
                            st.markdown("**Source Context:**")  # pragma: no cover
                            for src in res["sources"]:  # pragma: no cover
                                st.markdown(f"> *{src.strip()}*")  # pragma: no cover

                # Clean up
                os.unlink(tmp_path)  # pragma: no cover

            except Exception as e:  # pragma: no cover
                st.error(f"An error occurred: {str(e)}")  # pragma: no cover
                # Clean up if failed
                if 'tmp_path' in locals() and os.path.exists(tmp_path):  # pragma: no cover
                     os.unlink(tmp_path)  # pragma: no cover
