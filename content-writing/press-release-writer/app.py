import streamlit as st
import os
import sys

# Add parent directory to path just in case
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from agent.core import PressReleaseGenerator
from agent.tools import save_to_markdown, save_to_pdf

# Page Config
st.set_page_config(
    page_title="Press Release Writer AI",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {Config.THEME_BACKGROUND_COLOR};
        color: {Config.THEME_TEXT_COLOR};
    }}
    .stButton>button {{
        background-color: {Config.THEME_PRIMARY_COLOR};
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
    }}
    h1, h2, h3 {{
        font-family: 'Helvetica Neue', sans-serif;
        color: {Config.THEME_PRIMARY_COLOR} !important;
    }}
    .stTextInput>div>div>input {{
        background-color: #262730;
        color: white;
        border-radius: 5px;
        border: 1px solid #444;
    }}
    .stTextArea>div>div>textarea {{
        background-color: #262730;
        color: white;
        border-radius: 5px;
        border: 1px solid #444;
    }}
    /* Custom divider color */
    hr {{
        border-top: 1px solid #444;
    }}
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📰 AI Press Release Writer")
st.markdown("Generate professional, AP-style press releases in seconds with AI.")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    model_provider = st.selectbox("Model Provider", ["openai", "google"], index=0)

    # Check for env var first
    default_api_key = Config.OPENAI_API_KEY if model_provider == "openai" else Config.GEMINI_API_KEY

    api_key = st.text_input(
        f"{model_provider.capitalize()} API Key",
        type="password",
        value=default_api_key if default_api_key else ""
    )

    if api_key:
        os.environ[f"{model_provider.upper()}_API_KEY"] = api_key
        # Update config dynamically for this session if needed,
        # but the agent reads from env or config. Env is safer here.

    st.divider()
    st.info("Ensure you have set your API key correctly in .env or here.")

    st.markdown("### About")
    st.markdown("This tool uses advanced LLMs to draft press releases following AP style guidelines.")

# Main Input Area
col1, col2 = st.columns(2)

with col1:
    st.subheader("Product / Event Details")
    product_name = st.text_input("Product/Event Name", placeholder="e.g., SolarX Smart Battery")
    details = st.text_area("Key Details & Features", height=150, placeholder="Describe the product, launch date, key features, benefits...")
    tone = st.select_slider("Tone", options=["Strictly Professional", "Professional but Engaging", "Exciting & Bold"], value="Professional but Engaging")

with col2:
    st.subheader("Company & Contact")
    company_name = st.text_input("Company Name")
    company_description = st.text_area("Company Boilerplate (About Us)", height=100, placeholder="Brief description of the company...")
    contact_person = st.text_input("Contact Person Name & Title", placeholder="e.g. Jane Doe, CEO")
    media_contact = st.text_area("Media Contact Info", height=100, placeholder="Name\nEmail\nPhone\nWebsite")
    audience = st.text_input("Target Audience", placeholder="e.g., Tech Enthusiasts, Investors, General Public")

# Generate Button
if st.button("Generate Press Release", type="primary"):
    if not api_key:
        st.error("Please provide an API Key.")
    elif not all([product_name, details, company_name]):
        st.warning("Please fill in at least Product Name, Details, and Company Name.")
    else:
        with st.spinner("Drafting press release..."):
            try:
                # Initialize Agent
                agent = PressReleaseGenerator(model_provider=model_provider)

                # Generate Content
                raw_release = agent.generate_release(
                    product_name, details, company_name, company_description,
                    contact_person, media_contact, audience, tone
                )

                st.session_state['generated_release'] = raw_release
                st.success("Press Release Generated!")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Display Results
if 'generated_release' in st.session_state:
    st.divider()
    st.subheader("Generated Press Release")

    release_text = st.session_state['generated_release']
    st.text_area("Edit & Review", value=release_text, height=600)

    # Download Options
    st.subheader("Export")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            label="Download Markdown",
            data=release_text,
            file_name=f"{product_name.replace(' ', '_')}_press_release.md",
            mime="text/markdown"
        )
    with col_d2:
        try:
            pdf_path = f"{product_name.replace(' ', '_')}_press_release.pdf"
            # Create PDF
            save_to_pdf(release_text, pdf_path)

            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()

            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=pdf_path,
                mime="application/pdf"
            )

            # Clean up after reading
            os.remove(pdf_path)

        except Exception as e:
            st.warning(f"PDF Generation failed (requires fpdf): {e}")
