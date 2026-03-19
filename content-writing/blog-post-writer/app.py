import sys  # pragma: no cover
import os  # pragma: no cover
import streamlit as st  # pragma: no cover
import time  # pragma: no cover

# Ensure the current directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover

from agent.researcher import Researcher  # pragma: no cover
from agent.writer import Writer  # pragma: no cover
from agent.seo import SEOOptimizer  # pragma: no cover
from agent.utils import save_to_file, format_filename  # pragma: no cover
from config import OPENAI_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE  # pragma: no cover

# Page Configuration
st.set_page_config(  # pragma: no cover
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
st.markdown("""  # pragma: no cover
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
with st.sidebar:  # pragma: no cover
    st.image("https://python.langchain.com/img/favicon.ico", width=50)  # pragma: no cover
    st.title("Settings")  # pragma: no cover

    api_key = st.text_input("OpenAI API Key", value=OPENAI_API_KEY if OPENAI_API_KEY else "", type="password")  # pragma: no cover
    model_name = st.selectbox("Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)  # pragma: no cover
    temperature = st.slider("Temperature", 0.0, 1.0, DEFAULT_TEMPERATURE)  # pragma: no cover

    st.markdown("---")  # pragma: no cover
    st.markdown("### About")  # pragma: no cover
    st.info("This agent researches a topic, creates an outline, writes a full blog post, and optimizes it for SEO.")  # pragma: no cover

# Main Content
st.markdown('<div class="main-header">AI Blog Post Writer ✍️</div>', unsafe_allow_html=True)  # pragma: no cover
st.markdown('<div class="sub-header">Transform your ideas into SEO-optimized content in seconds.</div>', unsafe_allow_html=True)  # pragma: no cover

# Input
topic = st.text_input("Enter the topic for your blog post:", placeholder="e.g., The Future of Artificial Intelligence in Healthcare")  # pragma: no cover

if st.button("Generate Blog Post"):  # pragma: no cover
    if not api_key:  # pragma: no cover
        st.error("Please provide an OpenAI API Key in the sidebar.")  # pragma: no cover
    elif not topic:  # pragma: no cover
        st.warning("Please enter a topic.")  # pragma: no cover
    else:
        # Override config API key if provided
        os.environ["OPENAI_API_KEY"] = api_key  # pragma: no cover

        # Initialize Agents
        researcher = Researcher(model_name=model_name, temperature=temperature)  # pragma: no cover
        writer = Writer(model_name=model_name, temperature=temperature)  # pragma: no cover
        seo_optimizer = SEOOptimizer(model_name=model_name, temperature=temperature)  # pragma: no cover

        # Container for results
        results_container = st.container()  # pragma: no cover

        with results_container:  # pragma: no cover
            # Step 1: Research
            with st.status("🔍 Researching Topic...", expanded=True) as status:  # pragma: no cover
                st.write("Gathering information from the web...")  # pragma: no cover
                try:  # pragma: no cover
                    research_result = researcher.research(topic)  # pragma: no cover
                    research_summary = research_result['summary']  # pragma: no cover
                    st.success("Research Complete!")  # pragma: no cover
                    with st.expander("View Research Summary"):  # pragma: no cover
                        st.markdown(research_summary)  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.error(f"Research failed: {e}")  # pragma: no cover
                    status.update(state="error")  # pragma: no cover
                    st.stop()  # pragma: no cover

            # Step 2: Outline
            with st.status("📝 Creating Outline...", expanded=True) as status:  # pragma: no cover
                st.write("Structuring the blog post...")  # pragma: no cover
                try:  # pragma: no cover
                    outline = writer.create_outline(topic, research_summary)  # pragma: no cover
                    st.success("Outline Created!")  # pragma: no cover
                    with st.expander("View Outline"):  # pragma: no cover
                        st.markdown(outline)  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.error(f"Outline creation failed: {e}")  # pragma: no cover
                    status.update(state="error")  # pragma: no cover
                    st.stop()  # pragma: no cover

            # Step 3: Write Post
            with st.status("✍️ Writing Blog Post...", expanded=True) as status:  # pragma: no cover
                st.write("Drafting the content...")  # pragma: no cover
                try:  # pragma: no cover
                    blog_post = writer.write_post(topic, outline, research_summary)  # pragma: no cover
                    st.success("Drafting Complete!")  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.error(f"Writing failed: {e}")  # pragma: no cover
                    status.update(state="error")  # pragma: no cover
                    st.stop()  # pragma: no cover

            # Step 4: SEO
            with st.status("🚀 Optimizing for SEO...", expanded=True) as status:  # pragma: no cover
                st.write("Generating metadata and keywords...")  # pragma: no cover
                try:  # pragma: no cover
                    seo_result = seo_optimizer.optimize(topic, blog_post)  # pragma: no cover
                    seo_report = seo_result['seo_report']  # pragma: no cover
                    st.success("Optimization Complete!")  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.error(f"SEO optimization failed: {e}")  # pragma: no cover
                    status.update(state="error")  # pragma: no cover
                    st.stop()  # pragma: no cover

            # Final Display
            st.markdown("---")  # pragma: no cover

            col1, col2 = st.columns(2)  # pragma: no cover

            with col1:  # pragma: no cover
                st.header("📄 Final Blog Post")  # pragma: no cover
                st.markdown(blog_post)  # pragma: no cover

                # Download Button
                filename = format_filename(topic)  # pragma: no cover
                st.download_button(  # pragma: no cover
                    label="Download Markdown",
                    data=blog_post,
                    file_name=f"{filename}.md",
                    mime="text/markdown"
                )

            with col2:  # pragma: no cover
                st.header("📊 SEO Report")  # pragma: no cover
                st.markdown(seo_report)  # pragma: no cover

                # Download Button
                st.download_button(  # pragma: no cover
                    label="Download SEO Report",
                    data=seo_report,
                    file_name=f"{filename}-seo-report.md",
                    mime="text/markdown"
                )
