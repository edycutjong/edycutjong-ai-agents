import streamlit as st
import json
import os
import sys

# Ensure proper path for imports if running as script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.extractor import DesignTokenExtractor
from agent.parser import DesignParser
from agent.generator import DesignGenerator
from agent.models import TokenSet

# Page config
st.set_page_config(
    page_title="Design Token Extractor",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Premium UI"
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #1e3a8a;
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .token-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎨 Design Token Extractor")
st.markdown("Extract design tokens from your design specs instantly using AI.")

# Sidebar
with st.sidebar:
    st.header("Upload Spec")
    uploaded_file = st.file_uploader("Upload Design Spec", type=["json", "md", "txt"])

    st.markdown("---")
    st.info("Supported formats: JSON (Figma export), Markdown, Text.")

    if st.session_state.get("token_set"):
        if st.button("Clear Results"):
            if "token_set" in st.session_state:
                del st.session_state.token_set
            st.rerun()

# Main content
if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    file_type = uploaded_file.name.split(".")[-1]

    # Display preview
    with st.expander("📄 Source Preview", expanded=False):
        st.code(content, language=file_type if file_type != "txt" else "markdown")

    col1, col2 = st.columns([1, 4])
    with col1:
        extract_btn = st.button("Extract Tokens", type="primary")

    if extract_btn:
        with st.spinner("Analyzing design spec..."):
            try:
                # 1. Parse
                parsed_content = DesignParser.parse_content(content, file_type)

                # 2. Extract
                extractor = DesignTokenExtractor()
                token_set = extractor.extract(parsed_content)

                # Store in session state
                st.session_state.token_set = token_set
                st.success(f"Successfully extracted {len(token_set.tokens)} tokens!")

            except Exception as e:
                st.error(f"Error during extraction: {str(e)}")

# Display Results
if "token_set" in st.session_state:
    token_set = st.session_state.token_set

    st.divider()

    # Display Tokens
    st.subheader("Extracted Tokens")

    if not token_set.tokens:
        st.warning("No tokens found. Try adjusting your input.")
    else:
        # Group by type for display
        tokens_by_type = {}
        for token in token_set.tokens:
            t_type = token.type or "other"
            if t_type not in tokens_by_type:
                tokens_by_type[t_type] = []
            tokens_by_type[t_type].append(token)

        tabs = st.tabs(sorted(list(tokens_by_type.keys())))

        for i, (type_name, tokens) in enumerate(sorted(tokens_by_type.items())):
            with tabs[i]:
                # Use columns or dataframe
                data = [{"Name": t.name, "Value": t.value, "Description": t.description} for t in tokens]
                st.dataframe(data, use_container_width=True)

        # Export Section
        st.divider()
        st.subheader("💾 Export Formats")

        c1, c2, c3, c4 = st.columns(4)

        css_output = DesignGenerator.to_css(token_set)
        scss_output = DesignGenerator.to_scss(token_set)
        tailwind_output = DesignGenerator.to_tailwind(token_set)
        json_output = DesignGenerator.to_json(token_set)

        with c1:
            st.download_button("Download CSS", css_output, "tokens.css", "text/css")
        with c2:
            st.download_button("Download SCSS", scss_output, "_tokens.scss", "text/x-scss")
        with c3:
            st.download_button("Download Tailwind", tailwind_output, "tailwind.config.js", "application/javascript")
        with c4:
            st.download_button("Download JSON", json_output, "tokens.json", "application/json")

        # Preview Code
        with st.expander("Show Generated Code"):
            format_tab = st.tabs(["CSS", "SCSS", "Tailwind", "JSON"])
            with format_tab[0]: st.code(css_output, language="css")
            with format_tab[1]: st.code(scss_output, language="scss")
            with format_tab[2]: st.code(tailwind_output, language="javascript")
            with format_tab[3]: st.code(json_output, language="json")

else:
    # Placeholder / Guide
    if not uploaded_file:
        st.info("👆 Upload a file to get started.")
        st.markdown("""
        ### Example Input
        Create a markdown file with content like:
        ```markdown
        # Design System

        ## Colors
        - Primary: #3B82F6
        - Secondary: #10B981

        ## Typography
        - Base Size: 16px
        - Font Family: Inter, sans-serif
        ```
        """)
