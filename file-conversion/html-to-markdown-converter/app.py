import streamlit as st  # pragma: no cover
import sys  # pragma: no cover
import os  # pragma: no cover
import shutil  # pragma: no cover

# Add current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover

from agent.core import MarkdownConverterAgent  # pragma: no cover

st.set_page_config(  # pragma: no cover
    page_title="HTML to Markdown Converter",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for "Premium" look
st.markdown("""  # pragma: no cover
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #262730;
        color: white;
        border: 1px solid #4b4b4b;
    }
    .stButton>button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
    }
    h1 {
        text-align: center;
        color: #ff4b4b;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        margin-bottom: 1rem;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        color: #721c24;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("📝 HTML to Markdown Converter Agent")  # pragma: no cover
st.markdown("---")  # pragma: no cover

with st.sidebar:  # pragma: no cover
    st.header("Settings")  # pragma: no cover
    download_images = st.checkbox("Download Images", value=False, help="Extract and download images locally.")  # pragma: no cover
    output_dir = st.text_input("Output Directory", value="output")  # pragma: no cover
    st.markdown("### About")  # pragma: no cover
    st.info("This tool converts web pages to clean Markdown using an intelligent agent pipeline.")  # pragma: no cover

url = st.text_input("Enter URL to convert:", placeholder="https://example.com/article")  # pragma: no cover

if st.button("Convert"):  # pragma: no cover
    if not url:  # pragma: no cover
        st.error("Please enter a URL.")  # pragma: no cover
    else:
        with st.spinner("Converting..."):  # pragma: no cover
            try:  # pragma: no cover
                # Clean up output dir if needed or just use it
                agent = MarkdownConverterAgent(output_dir=output_dir, download_images=download_images)  # pragma: no cover
                result_path = agent.process_url(url)  # pragma: no cover

                if result_path and not result_path.startswith("Error"):  # pragma: no cover
                    st.success(f"Successfully converted!")  # pragma: no cover

                    # Read the file content
                    with open(result_path, "r", encoding="utf-8") as f:  # pragma: no cover
                        markdown_content = f.read()  # pragma: no cover

                    col1, col2 = st.columns(2)  # pragma: no cover

                    with col1:  # pragma: no cover
                        st.subheader("Markdown Preview")  # pragma: no cover
                        st.text_area("Source", value=markdown_content, height=600)  # pragma: no cover

                    with col2:  # pragma: no cover
                        st.subheader("Rendered Preview")  # pragma: no cover
                        st.markdown(markdown_content)  # pragma: no cover

                    # Download button
                    st.download_button(  # pragma: no cover
                        label="Download Markdown",
                        data=markdown_content,
                        file_name=os.path.basename(result_path),
                        mime="text/markdown"
                    )

                    if download_images:  # pragma: no cover
                        # Zip images if any
                        img_dir = os.path.join(output_dir, "images")  # pragma: no cover
                        if os.path.exists(img_dir) and os.listdir(img_dir):  # pragma: no cover
                            shutil.make_archive("images", 'zip', img_dir)  # pragma: no cover
                            with open("images.zip", "rb") as f:  # pragma: no cover
                                st.download_button(  # pragma: no cover
                                    label="Download Images (ZIP)",
                                    data=f,
                                    file_name="images.zip",
                                    mime="application/zip"
                                )
                else:
                    st.error(f"Conversion failed: {result_path}")  # pragma: no cover
            except Exception as e:  # pragma: no cover
                st.error(f"An error occurred: {e}")  # pragma: no cover

st.markdown("---")  # pragma: no cover
st.caption("Built with ❤️ by Jules")  # pragma: no cover
