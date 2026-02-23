import streamlit as st
import sys
import os

# Add current directory to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from config import Config
from agent import TrendMonitor, ContentGenerator, Scheduler, Analytics, EngagementManager

# Page Config
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon=Config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown(f"""
    <style>
    .stApp {{
        background: {Config.THEME_BG_GRADIENT};
        color: white;
    }}
    .sidebar .sidebar-content {{
        background-color: rgba(30, 27, 75, 0.9);
    }}
    h1, h2, h3 {{
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, {Config.THEME_COLOR_PRIMARY}, {Config.THEME_COLOR_ACCENT});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .stButton>button {{
        background: linear-gradient(90deg, {Config.THEME_COLOR_PRIMARY}, {Config.THEME_COLOR_SECONDARY});
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }}
    .card {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }}
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = Scheduler()
if 'analytics' not in st.session_state:
    st.session_state.analytics = Analytics()
if 'trends' not in st.session_state:
    st.session_state.trends = TrendMonitor()
if 'generator' not in st.session_state:
    st.session_state.generator = ContentGenerator() # API key will be updated from sidebar
if 'engagement' not in st.session_state:
    st.session_state.engagement = EngagementManager(st.session_state.generator)

# Sidebar
with st.sidebar:
    st.title(f"{Config.APP_ICON} {Config.APP_NAME}")

    st.markdown("---")

    menu = st.radio(
        "Navigation",
        ["Dashboard", "Create Content", "Schedule", "Engage", "Settings"],
        index=0
    )

    st.markdown("---")

    st.subheader("⚙️ Quick Settings")
    api_key = st.text_input("OpenAI API Key", type="password", value=Config.get_api_key() or "")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        # Re-initialize generator with new key if changed
        if st.session_state.generator.api_key != api_key:
            st.session_state.generator = ContentGenerator(api_key=api_key)
            st.session_state.engagement = EngagementManager(st.session_state.generator)

    brand_voice = st.text_area("Brand Voice", value="Professional, engaging, and tech-savvy", height=100)
    if brand_voice != st.session_state.generator.brand_voice:
         st.session_state.generator.brand_voice = brand_voice

# Main Content Routing
if menu == "Dashboard":
    st.header("Dashboard")
    st.write("Welcome to your AI Social Media Manager.")

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Followers", value="12.5K", delta="+120")
    with col2:
        st.metric(label="Avg. Engagement", value="4.2%", delta="+0.5%")
    with col3:
        st.metric(label="Scheduled Posts", value=str(len(st.session_state.scheduler.get_queue("Draft"))), delta="Active")

    st.markdown("---")

    # Analytics Chart
    st.subheader("📈 Growth Overview")
    growth_df = st.session_state.analytics.get_growth_stats()
    st.line_chart(growth_df.set_index("Date")[["Followers", "Engagement"]])

    st.markdown("---")

    # Trends Preview
    st.subheader("🔥 Trending Now")
    trends = st.session_state.trends.get_trends()

    trend_cols = st.columns(3)
    for i, trend in enumerate(trends[:3]):
        with trend_cols[i]:
            st.markdown(f"""
            <div class="card">
                <h4>{trend['topic']}</h4>
                <p style="color: #aaa; font-size: 0.9em;">{trend['volume']} • {trend['sentiment']}</p>
                <p style="font-size: 0.8em;">{trend['source']}</p>
            </div>
            """, unsafe_allow_html=True)

elif menu == "Create Content":
    st.header("Create New Content")

    col1, col2 = st.columns([2, 1])

    with col1:
        topic = st.text_input("What is the post about?", placeholder="e.g., The future of AI Agents")
        platform = st.selectbox("Select Platform", ["Twitter", "LinkedIn", "Instagram"])

        if st.button("Generate Draft"):
            with st.spinner("Generating content..."):
                draft = st.session_state.generator.generate_draft(topic, platform)
                st.session_state.current_draft = draft

                # Generate Image Prompt as well
                image_prompt = st.session_state.generator.generate_image_prompt(topic, platform)
                st.session_state.current_image_prompt = image_prompt

    with col2:
        st.subheader("Draft Preview")
        if 'current_draft' in st.session_state:
            draft_content = st.text_area("Post Content", value=st.session_state.current_draft, height=200)
            img_prompt = st.text_area("Image Prompt", value=st.session_state.current_image_prompt, height=100)

            if st.button("Add to Schedule"):
                st.session_state.scheduler.add_draft(
                    topic,
                    platform,
                    draft_content,
                    img_prompt
                )
                st.success("Draft added to schedule!")
                # Clear draft
                del st.session_state.current_draft
                del st.session_state.current_image_prompt
                st.rerun()

elif menu == "Schedule":
    st.header("Content Schedule")

    tab1, tab2 = st.tabs(["Upcoming", "Published"])

    with tab1:
        queue = st.session_state.scheduler.get_queue("Draft")
        if not queue:
            st.info("No scheduled posts. Go to 'Create Content' to add some!")
        else:
            for post in queue:
                with st.expander(f"{post['platform']}: {post['topic']} ({post['scheduled_time']})"):
                    st.write(post['content'])
                    st.caption(f"Image Prompt: {post['image_prompt']}")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("Publish Now", key=f"pub_{post['id']}"):
                            st.session_state.scheduler.update_status(post['id'], "Published")
                            st.success("Post published!")
                            st.rerun()
                    with col_b:
                        if st.button("Delete", key=f"del_{post['id']}"):
                            st.session_state.scheduler.delete_draft(post['id'])
                            st.warning("Post deleted.")
                            st.rerun()

    with tab2:
        published = st.session_state.scheduler.get_queue("Published")
        if not published:
            st.info("No published posts yet.")
        else:
            for post in published:
                st.markdown(f"**{post['platform']}** - {post['topic']}")
                st.text(post['content'])
                st.markdown("---")

elif menu == "Engage":
    st.header("Community Engagement")

    st.write("Review and reply to recent comments.")

    if 'replies' not in st.session_state:
        st.session_state.replies = {}

    comments = st.session_state.engagement.get_pending_comments()

    for comment in comments:
        with st.container():
            st.markdown(f"""
            <div class="card">
                <h5>{comment['user']} on {comment['platform']}</h5>
                <p>"{comment['text']}"</p>
                <span style="background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 4px; font-size: 0.8em;">{comment['sentiment']}</span>
            </div>
            """, unsafe_allow_html=True)

            reply_key = f"reply_{comment['id']}"

            if st.button("Generate Reply Suggestion", key=f"reply_btn_{comment['id']}"):
                with st.spinner("Generating reply..."):
                    reply = st.session_state.engagement.suggest_reply(comment)
                    st.session_state.replies[reply_key] = reply

            if reply_key in st.session_state.replies:
                st.text_area("Suggested Reply", value=st.session_state.replies[reply_key], height=100, key=f"reply_text_{comment['id']}")
                if st.button("Post Reply", key=f"post_reply_{comment['id']}"):
                     st.success(f"Reply posted to {comment['platform']}!")
                     del st.session_state.replies[reply_key]
                     st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

elif menu == "Settings":
    st.header("Application Settings")
    st.write("Manage your preferences and integrations.")
    # Placeholder for Settings tab logic
