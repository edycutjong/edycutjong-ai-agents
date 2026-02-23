import streamlit as st
import tempfile
import os
import shutil

# Add the current directory to sys.path to allow imports
import sys
sys.path.append(os.path.dirname(__file__))

from agent.detector import HallucinationDetector

st.set_page_config(
    page_title="AI Hallucination Detector",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS for Premium UI ---
st.markdown("""
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
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620536.png", width=100) # Placeholder icon
    st.title("Settings")

    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API Key if not set in .env")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("1. Upload a **Source Document** (PDF or TXT).")
    st.markdown("2. Paste the **AI Generated Text** you want to verify.")
    st.markdown("3. Click **Analyze** to detect hallucinations.")

    st.markdown("---")
    st.info("Built with LangChain & Streamlit")

# --- Main Content ---
st.title("🕵️ AI Hallucination Detector")
st.markdown("### Verify AI outputs against source documents with confidence.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Source Document")
    uploaded_file = st.file_uploader("Upload reference document", type=["pdf", "txt"])

with col2:
    st.subheader("2. AI Output")
    ai_text = st.text_area("Paste the text to verify here", height=200, placeholder="The generated summary or content...")

if st.button("Analyze Content"):
    if not uploaded_file or not ai_text:
        st.error("Please upload a source document and provide AI text.")
    elif not os.environ.get("OPENAI_API_KEY"):
        st.error("Please provide an OpenAI API Key.")
    else:
        with st.spinner("Analyzing claims and verifying against source..."):
            try:
                # Save uploaded file to temp
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    shutil.copyfileobj(uploaded_file, tmp_file)
                    tmp_path = tmp_file.name

                # Initialize Detector
                detector = HallucinationDetector()

                # Run Analysis
                # We need to adapt the method signature if I changed it.
                # I defined process(ai_text, source_file_path)

                # First, process document into vector store
                vectorstore = detector.process_document(tmp_path)

                # Extract claims
                claims = detector.extract_claims(ai_text)

                results = []
                verified_count = 0

                progress_bar = st.progress(0)
                status_text = st.empty()

                total_claims = len(claims)

                for i, claim in enumerate(claims):
                    status_text.text(f"Verifying claim {i+1}/{total_claims}...")
                    verification = detector.verify_claim(claim, vectorstore)
                    results.append(verification)

                    if verification.get("status") == "VERIFIED":
                        verified_count += 1

                    progress_bar.progress((i + 1) / total_claims)

                status_text.empty()
                progress_bar.empty()

                # Calculate Score
                score = (verified_count / total_claims) * 100 if total_claims > 0 else 0

                # --- Display Results ---
                st.markdown("---")
                st.subheader("Analysis Report")

                # Score Card
                score_color = "green" if score > 80 else "orange" if score > 50 else "red"
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; background-color: #fff; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3>Trust Score</h3>
                    <h1 style="color: {score_color}; font-size: 4rem; margin: 0;">{score:.1f}%</h1>
                    <p>{verified_count} of {total_claims} claims verified</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Detailed Claims
                st.subheader("Detailed Claim Analysis")

                for res in results:
                    status = res.get("status", "UNKNOWN")
                    confidence = res.get("confidence", 0.0)
                    claim_text = res.get("claim", "")
                    explanation = res.get("explanation", "")

                    icon = "✅" if status == "VERIFIED" else "❌" if status == "HALLUCINATION" or status == "CONTRADICTED" else "⚠️"
                    css_class = "claim-verified" if status == "VERIFIED" else "claim-hallucination" if status == "HALLUCINATION" or status == "CONTRADICTED" else "claim-unsupported"

                    with st.expander(f"{icon} {claim_text[:80]}..."):
                        st.markdown(f"""
                        <div class="{css_class}">
                            <strong>Status:</strong> {status}<br>
                            <strong>Confidence:</strong> {confidence}<br>
                            <strong>Claim:</strong> {claim_text}
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"**Explanation:** {explanation}")

                        if res.get("sources"):
                            st.markdown("**Source Context:**")
                            for src in res["sources"]:
                                st.markdown(f"> *{src.strip()}*")

                # Clean up
                os.unlink(tmp_path)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                # Clean up if failed
                if 'tmp_path' in locals() and os.path.exists(tmp_path):
                     os.unlink(tmp_path)
