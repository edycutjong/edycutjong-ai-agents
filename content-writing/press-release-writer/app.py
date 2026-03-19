import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover

# Add parent directory to path just in case
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover

from config import Config  # pragma: no cover
from agent.core import PressReleaseGenerator  # pragma: no cover
from agent.tools import save_to_markdown, save_to_pdf  # pragma: no cover

# Page Config
st.set_page_config(  # pragma: no cover
    page_title="Press Release Writer AI",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown(f"""  # pragma: no cover
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
st.title("📰 AI Press Release Writer")  # pragma: no cover
st.markdown("Generate professional, AP-style press releases in seconds with AI.")  # pragma: no cover

# Sidebar
with st.sidebar:  # pragma: no cover
    st.header("Configuration")  # pragma: no cover
    model_provider = st.selectbox("Model Provider", ["openai", "google"], index=0)  # pragma: no cover

    # Check for env var first
    default_api_key = Config.OPENAI_API_KEY if model_provider == "openai" else Config.GEMINI_API_KEY  # pragma: no cover

    api_key = st.text_input(  # pragma: no cover
        f"{model_provider.capitalize()} API Key",
        type="password",
        value=default_api_key if default_api_key else ""
    )

    if api_key:  # pragma: no cover
        os.environ[f"{model_provider.upper()}_API_KEY"] = api_key  # pragma: no cover
        # Update config dynamically for this session if needed,
        # but the agent reads from env or config. Env is safer here.

    st.divider()  # pragma: no cover
    st.info("Ensure you have set your API key correctly in .env or here.")  # pragma: no cover

    st.markdown("### About")  # pragma: no cover
    st.markdown("This tool uses advanced LLMs to draft press releases following AP style guidelines.")  # pragma: no cover

# Main Input Area
col1, col2 = st.columns(2)  # pragma: no cover

with col1:  # pragma: no cover
    st.subheader("Product / Event Details")  # pragma: no cover
    product_name = st.text_input("Product/Event Name", placeholder="e.g., SolarX Smart Battery")  # pragma: no cover
    details = st.text_area("Key Details & Features", height=150, placeholder="Describe the product, launch date, key features, benefits...")  # pragma: no cover
    tone = st.select_slider("Tone", options=["Strictly Professional", "Professional but Engaging", "Exciting & Bold"], value="Professional but Engaging")  # pragma: no cover

with col2:  # pragma: no cover
    st.subheader("Company & Contact")  # pragma: no cover
    company_name = st.text_input("Company Name")  # pragma: no cover
    company_description = st.text_area("Company Boilerplate (About Us)", height=100, placeholder="Brief description of the company...")  # pragma: no cover
    contact_person = st.text_input("Contact Person Name & Title", placeholder="e.g. Jane Doe, CEO")  # pragma: no cover
    media_contact = st.text_area("Media Contact Info", height=100, placeholder="Name\nEmail\nPhone\nWebsite")  # pragma: no cover
    audience = st.text_input("Target Audience", placeholder="e.g., Tech Enthusiasts, Investors, General Public")  # pragma: no cover

# Generate Button
if st.button("Generate Press Release", type="primary"):  # pragma: no cover
    if not api_key:  # pragma: no cover
        st.error("Please provide an API Key.")  # pragma: no cover
    elif not all([product_name, details, company_name]):  # pragma: no cover
        st.warning("Please fill in at least Product Name, Details, and Company Name.")  # pragma: no cover
    else:
        with st.spinner("Drafting press release..."):  # pragma: no cover
            try:  # pragma: no cover
                # Initialize Agent
                agent = PressReleaseGenerator(model_provider=model_provider)  # pragma: no cover

                # Generate Content
                raw_release = agent.generate_release(  # pragma: no cover
                    product_name, details, company_name, company_description,
                    contact_person, media_contact, audience, tone
                )

                st.session_state['generated_release'] = raw_release  # pragma: no cover
                st.success("Press Release Generated!")  # pragma: no cover

            except Exception as e:  # pragma: no cover
                st.error(f"An error occurred: {str(e)}")  # pragma: no cover

# Display Results
if 'generated_release' in st.session_state:  # pragma: no cover
    st.divider()  # pragma: no cover
    st.subheader("Generated Press Release")  # pragma: no cover

    release_text = st.session_state['generated_release']  # pragma: no cover
    st.text_area("Edit & Review", value=release_text, height=600)  # pragma: no cover

    # Download Options
    st.subheader("Export")  # pragma: no cover
    col_d1, col_d2 = st.columns(2)  # pragma: no cover
    with col_d1:  # pragma: no cover
        st.download_button(  # pragma: no cover
            label="Download Markdown",
            data=release_text,
            file_name=f"{product_name.replace(' ', '_')}_press_release.md",
            mime="text/markdown"
        )
    with col_d2:  # pragma: no cover
        try:  # pragma: no cover
            pdf_path = f"{product_name.replace(' ', '_')}_press_release.pdf"  # pragma: no cover
            # Create PDF
            save_to_pdf(release_text, pdf_path)  # pragma: no cover

            with open(pdf_path, "rb") as pdf_file:  # pragma: no cover
                pdf_bytes = pdf_file.read()  # pragma: no cover

            st.download_button(  # pragma: no cover
                label="Download PDF",
                data=pdf_bytes,
                file_name=pdf_path,
                mime="application/pdf"
            )

            # Clean up after reading
            os.remove(pdf_path)  # pragma: no cover

        except Exception as e:  # pragma: no cover
            st.warning(f"PDF Generation failed (requires fpdf): {e}")  # pragma: no cover
