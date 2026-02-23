import streamlit as st
import time
import logging
from datetime import datetime

# Adjust import paths
try:
    from agent.fetcher import fetch_rss_feed
    from agent.processor import process_articles
    from agent.formatter import format_newsletter_markdown, format_newsletter_html
    from config import APP_TITLE, APP_ICON, DEFAULT_RSS_FEEDS, DEFAULT_TOPICS
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
    from agent.fetcher import fetch_rss_feed
    from agent.processor import process_articles
    from agent.formatter import format_newsletter_markdown, format_newsletter_html
    from config import APP_TITLE, APP_ICON, DEFAULT_RSS_FEEDS, DEFAULT_TOPICS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page Config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
        height: 50px;
        font-weight: bold;
    }
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    h1 {
        color: #2c3e50;
    }
    h2 {
        color: #e67e22;
    }
    .stProgress > div > div > div > div {
        background-color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2965/2965363.png", width=50)
        st.title("Settings")

        with st.expander("API Configuration", expanded=True):
            api_provider = st.selectbox("LLM Provider", ["OpenAI", "Google Gemini"])
            api_key = st.text_input(
                f"{api_provider} API Key",
                type="password",
                help=f"Enter your {api_provider} API Key here."
            )

        with st.expander("Content Sources", expanded=True):
            rss_feeds_input = st.text_area(
                "RSS Feeds (one URL per line)",
                value="\n".join(DEFAULT_RSS_FEEDS),
                height=150
            )

        with st.expander("Curator Preferences", expanded=True):
            topics_input = st.text_area(
                "Topics of Interest (comma separated)",
                value=", ".join(DEFAULT_TOPICS),
                height=100
            )
            lookback_days = st.slider("Lookback Period (Days)", 1, 30, 3)
            min_score = st.slider("Minimum Importance Score", 1, 10, 5)

    # Main Content
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"{APP_ICON} {APP_TITLE}")
        st.markdown("Generate a curated newsletter from your favorite RSS feeds using AI.")

    with col2:
        st.write("")
        st.write("")
        generate_btn = st.button("🚀 Generate Newsletter")

    if generate_btn:
        if not api_key:
            st.error("⚠️ Please enter an API Key in the sidebar.")
            st.stop()

        status_container = st.container()
        progress_bar = st.progress(0)

        try:
            # 1. Fetching
            with status_container:
                st.info("📡 Fetching articles from RSS feeds...")

            feeds = [url.strip() for url in rss_feeds_input.splitlines() if url.strip()]
            all_articles = []

            total_feeds = len(feeds)
            for i, url in enumerate(feeds):
                try:
                    articles = fetch_rss_feed(url, days=lookback_days)
                    all_articles.extend(articles)
                    progress_bar.progress((i + 1) / total_feeds * 0.3) # Up to 30%
                except Exception as e:
                    st.warning(f"Failed to fetch {url}: {e}")

            with status_container:
                st.success(f"✅ Fetched {len(all_articles)} articles from {total_feeds} sources.")
                time.sleep(1)
                st.info("🧠 Analyzing articles with AI (this may take a moment)...")

            # 2. Processing
            topics_list = [t.strip() for t in topics_input.split(",") if t.strip()]

            # Mocking progress for processing since it's one call (or batch loop)
            processed_articles = process_articles(
                all_articles,
                topics_list,
                api_key,
                provider="openai" if api_provider == "OpenAI" else "google"
            )

            progress_bar.progress(0.8) # 80%

            # Filter by min score
            final_articles = [a for a in processed_articles if a.get("score", 0) >= min_score]

            with status_container:
                st.success(f"✅ Curated {len(final_articles)} high-quality articles.")
                time.sleep(1)
                st.info("📝 Formatting newsletter...")

            # 3. Formatting
            newsletter_md = format_newsletter_markdown(
                final_articles,
                title=f"Curated Tech News - {datetime.now().strftime('%Y-%m-%d')}"
            )
            newsletter_html = format_newsletter_html(
                final_articles,
                title=f"Curated Tech News - {datetime.now().strftime('%Y-%m-%d')}"
            )

            progress_bar.progress(1.0) # 100%
            time.sleep(0.5)
            status_container.empty()

            # Results
            tab1, tab2, tab3 = st.tabs(["📄 Preview", "📝 Markdown Code", "🌐 HTML Code"])

            with tab1:
                st.markdown(newsletter_md)

            with tab2:
                st.code(newsletter_md, language="markdown")
                st.download_button(
                    label="Download Markdown",
                    data=newsletter_md,
                    file_name=f"newsletter_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )

            with tab3:
                st.code(newsletter_html, language="html")
                st.download_button(
                    label="Download HTML",
                    data=newsletter_html,
                    file_name=f"newsletter_{datetime.now().strftime('%Y%m%d')}.html",
                    mime="text/html"
                )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logger.exception("Error in main loop")

if __name__ == "__main__":
    main()
