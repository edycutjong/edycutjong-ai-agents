import streamlit as st
import sys
import os
import shutil

# Add current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.core import MarkdownConverterAgent

st.set_page_config(
    page_title="HTML to Markdown Converter",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for "Premium" look
st.markdown("""
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

st.title("📝 HTML to Markdown Converter Agent")
st.markdown("---")

with st.sidebar:
    st.header("Settings")
    download_images = st.checkbox("Download Images", value=False, help="Extract and download images locally.")
    output_dir = st.text_input("Output Directory", value="output")
    st.markdown("### About")
    st.info("This tool converts web pages to clean Markdown using an intelligent agent pipeline.")

url = st.text_input("Enter URL to convert:", placeholder="https://example.com/article")

if st.button("Convert"):
    if not url:
        st.error("Please enter a URL.")
    else:
        with st.spinner("Converting..."):
            try:
                # Clean up output dir if needed or just use it
                agent = MarkdownConverterAgent(output_dir=output_dir, download_images=download_images)
                result_path = agent.process_url(url)

                if result_path and not result_path.startswith("Error"):
                    st.success(f"Successfully converted!")

                    # Read the file content
                    with open(result_path, "r", encoding="utf-8") as f:
                        markdown_content = f.read()

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Markdown Preview")
                        st.text_area("Source", value=markdown_content, height=600)

                    with col2:
                        st.subheader("Rendered Preview")
                        st.markdown(markdown_content)

                    # Download button
                    st.download_button(
                        label="Download Markdown",
                        data=markdown_content,
                        file_name=os.path.basename(result_path),
                        mime="text/markdown"
                    )

                    if download_images:
                        # Zip images if any
                        img_dir = os.path.join(output_dir, "images")
                        if os.path.exists(img_dir) and os.listdir(img_dir):
                            shutil.make_archive("images", 'zip', img_dir)
                            with open("images.zip", "rb") as f:
                                st.download_button(
                                    label="Download Images (ZIP)",
                                    data=f,
                                    file_name="images.zip",
                                    mime="application/zip"
                                )
                else:
                    st.error(f"Conversion failed: {result_path}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Built with ❤️ by Jules")
