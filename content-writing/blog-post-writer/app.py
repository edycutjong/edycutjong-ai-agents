import sys
import os
import streamlit as st
import time

# Ensure the current directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.researcher import Researcher
from agent.writer import Writer
from agent.seo import SEOOptimizer
from agent.utils import save_to_file, format_filename
from config import OPENAI_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE

# Page Configuration
st.set_page_config(
    page_title="AI Blog Post Writer",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/langchain-ai/langchain',
        'Report a bug': "https://github.com/langchain-ai/langchain/issues",
        'About': "# AI Blog Post Writer\nPowered by LangChain, OpenAI, and Streamlit."
    }
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .main-header {
        font-size: 3rem;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-container {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #262730;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://python.langchain.com/img/favicon.ico", width=50)
    st.title("Settings")

    api_key = st.text_input("OpenAI API Key", value=OPENAI_API_KEY if OPENAI_API_KEY else "", type="password")
    model_name = st.selectbox("Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)
    temperature = st.slider("Temperature", 0.0, 1.0, DEFAULT_TEMPERATURE)

    st.markdown("---")
    st.markdown("### About")
    st.info("This agent researches a topic, creates an outline, writes a full blog post, and optimizes it for SEO.")

# Main Content
st.markdown('<div class="main-header">AI Blog Post Writer ✍️</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform your ideas into SEO-optimized content in seconds.</div>', unsafe_allow_html=True)

# Input
topic = st.text_input("Enter the topic for your blog post:", placeholder="e.g., The Future of Artificial Intelligence in Healthcare")

if st.button("Generate Blog Post"):
    if not api_key:
        st.error("Please provide an OpenAI API Key in the sidebar.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        # Override config API key if provided
        os.environ["OPENAI_API_KEY"] = api_key

        # Initialize Agents
        researcher = Researcher(model_name=model_name, temperature=temperature)
        writer = Writer(model_name=model_name, temperature=temperature)
        seo_optimizer = SEOOptimizer(model_name=model_name, temperature=temperature)

        # Container for results
        results_container = st.container()

        with results_container:
            # Step 1: Research
            with st.status("🔍 Researching Topic...", expanded=True) as status:
                st.write("Gathering information from the web...")
                try:
                    research_result = researcher.research(topic)
                    research_summary = research_result['summary']
                    st.success("Research Complete!")
                    with st.expander("View Research Summary"):
                        st.markdown(research_summary)
                except Exception as e:
                    st.error(f"Research failed: {e}")
                    status.update(state="error")
                    st.stop()

            # Step 2: Outline
            with st.status("📝 Creating Outline...", expanded=True) as status:
                st.write("Structuring the blog post...")
                try:
                    outline = writer.create_outline(topic, research_summary)
                    st.success("Outline Created!")
                    with st.expander("View Outline"):
                        st.markdown(outline)
                except Exception as e:
                    st.error(f"Outline creation failed: {e}")
                    status.update(state="error")
                    st.stop()

            # Step 3: Write Post
            with st.status("✍️ Writing Blog Post...", expanded=True) as status:
                st.write("Drafting the content...")
                try:
                    blog_post = writer.write_post(topic, outline, research_summary)
                    st.success("Drafting Complete!")
                except Exception as e:
                    st.error(f"Writing failed: {e}")
                    status.update(state="error")
                    st.stop()

            # Step 4: SEO
            with st.status("🚀 Optimizing for SEO...", expanded=True) as status:
                st.write("Generating metadata and keywords...")
                try:
                    seo_result = seo_optimizer.optimize(topic, blog_post)
                    seo_report = seo_result['seo_report']
                    st.success("Optimization Complete!")
                except Exception as e:
                    st.error(f"SEO optimization failed: {e}")
                    status.update(state="error")
                    st.stop()

            # Final Display
            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.header("📄 Final Blog Post")
                st.markdown(blog_post)

                # Download Button
                filename = format_filename(topic)
                st.download_button(
                    label="Download Markdown",
                    data=blog_post,
                    file_name=f"{filename}.md",
                    mime="text/markdown"
                )

            with col2:
                st.header("📊 SEO Report")
                st.markdown(seo_report)

                # Download Button
                st.download_button(
                    label="Download SEO Report",
                    data=seo_report,
                    file_name=f"{filename}-seo-report.md",
                    mime="text/markdown"
                )
