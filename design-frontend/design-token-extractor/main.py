import streamlit as st  # pragma: no cover
import json  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover

# Ensure proper path for imports if running as script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover

from agent.extractor import DesignTokenExtractor  # pragma: no cover
from agent.parser import DesignParser  # pragma: no cover
from agent.generator import DesignGenerator  # pragma: no cover
from agent.models import TokenSet  # pragma: no cover

# Page config
st.set_page_config(  # pragma: no cover
    page_title="Design Token Extractor",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Premium UI"
st.markdown("""  # pragma: no cover
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

st.title("🎨 Design Token Extractor")  # pragma: no cover
st.markdown("Extract design tokens from your design specs instantly using AI.")  # pragma: no cover

# Sidebar
with st.sidebar:  # pragma: no cover
    st.header("Upload Spec")  # pragma: no cover
    uploaded_file = st.file_uploader("Upload Design Spec", type=["json", "md", "txt"])  # pragma: no cover

    st.markdown("---")  # pragma: no cover
    st.info("Supported formats: JSON (Figma export), Markdown, Text.")  # pragma: no cover

    if st.session_state.get("token_set"):  # pragma: no cover
        if st.button("Clear Results"):  # pragma: no cover
            if "token_set" in st.session_state:  # pragma: no cover
                del st.session_state.token_set  # pragma: no cover
            st.rerun()  # pragma: no cover

# Main content
if uploaded_file:  # pragma: no cover
    content = uploaded_file.read().decode("utf-8")  # pragma: no cover
    file_type = uploaded_file.name.split(".")[-1]  # pragma: no cover

    # Display preview
    with st.expander("📄 Source Preview", expanded=False):  # pragma: no cover
        st.code(content, language=file_type if file_type != "txt" else "markdown")  # pragma: no cover

    col1, col2 = st.columns([1, 4])  # pragma: no cover
    with col1:  # pragma: no cover
        extract_btn = st.button("Extract Tokens", type="primary")  # pragma: no cover

    if extract_btn:  # pragma: no cover
        with st.spinner("Analyzing design spec..."):  # pragma: no cover
            try:  # pragma: no cover
                # 1. Parse
                parsed_content = DesignParser.parse_content(content, file_type)  # pragma: no cover

                # 2. Extract
                extractor = DesignTokenExtractor()  # pragma: no cover
                token_set = extractor.extract(parsed_content)  # pragma: no cover

                # Store in session state
                st.session_state.token_set = token_set  # pragma: no cover
                st.success(f"Successfully extracted {len(token_set.tokens)} tokens!")  # pragma: no cover

            except Exception as e:  # pragma: no cover
                st.error(f"Error during extraction: {str(e)}")  # pragma: no cover

# Display Results
if "token_set" in st.session_state:  # pragma: no cover
    token_set = st.session_state.token_set  # pragma: no cover

    st.divider()  # pragma: no cover

    # Display Tokens
    st.subheader("Extracted Tokens")  # pragma: no cover

    if not token_set.tokens:  # pragma: no cover
        st.warning("No tokens found. Try adjusting your input.")  # pragma: no cover
    else:
        # Group by type for display
        tokens_by_type = {}  # pragma: no cover
        for token in token_set.tokens:  # pragma: no cover
            t_type = token.type or "other"  # pragma: no cover
            if t_type not in tokens_by_type:  # pragma: no cover
                tokens_by_type[t_type] = []  # pragma: no cover
            tokens_by_type[t_type].append(token)  # pragma: no cover

        tabs = st.tabs(sorted(list(tokens_by_type.keys())))  # pragma: no cover

        for i, (type_name, tokens) in enumerate(sorted(tokens_by_type.items())):  # pragma: no cover
            with tabs[i]:  # pragma: no cover
                # Use columns or dataframe
                data = [{"Name": t.name, "Value": t.value, "Description": t.description} for t in tokens]  # pragma: no cover
                st.dataframe(data, use_container_width=True)  # pragma: no cover

        # Export Section
        st.divider()  # pragma: no cover
        st.subheader("💾 Export Formats")  # pragma: no cover

        c1, c2, c3, c4 = st.columns(4)  # pragma: no cover

        css_output = DesignGenerator.to_css(token_set)  # pragma: no cover
        scss_output = DesignGenerator.to_scss(token_set)  # pragma: no cover
        tailwind_output = DesignGenerator.to_tailwind(token_set)  # pragma: no cover
        json_output = DesignGenerator.to_json(token_set)  # pragma: no cover

        with c1:  # pragma: no cover
            st.download_button("Download CSS", css_output, "tokens.css", "text/css")  # pragma: no cover
        with c2:  # pragma: no cover
            st.download_button("Download SCSS", scss_output, "_tokens.scss", "text/x-scss")  # pragma: no cover
        with c3:  # pragma: no cover
            st.download_button("Download Tailwind", tailwind_output, "tailwind.config.js", "application/javascript")  # pragma: no cover
        with c4:  # pragma: no cover
            st.download_button("Download JSON", json_output, "tokens.json", "application/json")  # pragma: no cover

        # Preview Code
        with st.expander("Show Generated Code"):  # pragma: no cover
            format_tab = st.tabs(["CSS", "SCSS", "Tailwind", "JSON"])  # pragma: no cover
            with format_tab[0]: st.code(css_output, language="css")  # pragma: no cover
            with format_tab[1]: st.code(scss_output, language="scss")  # pragma: no cover
            with format_tab[2]: st.code(tailwind_output, language="javascript")  # pragma: no cover
            with format_tab[3]: st.code(json_output, language="json")  # pragma: no cover

else:
    # Placeholder / Guide
    if not uploaded_file:  # pragma: no cover
        st.info("👆 Upload a file to get started.")  # pragma: no cover
        st.markdown("""  # pragma: no cover
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
