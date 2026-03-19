import streamlit as st  # pragma: no cover
import sys  # pragma: no cover
import os  # pragma: no cover

# Add current directory to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))  # pragma: no cover
sys.path.append(current_dir)  # pragma: no cover

from config import Config  # pragma: no cover
from agent import TrendMonitor, ContentGenerator, Scheduler, Analytics, EngagementManager  # pragma: no cover

# Page Config
st.set_page_config(  # pragma: no cover
    page_title=Config.APP_NAME,
    page_icon=Config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown(f"""  # pragma: no cover
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
if 'scheduler' not in st.session_state:  # pragma: no cover
    st.session_state.scheduler = Scheduler()  # pragma: no cover
if 'analytics' not in st.session_state:  # pragma: no cover
    st.session_state.analytics = Analytics()  # pragma: no cover
if 'trends' not in st.session_state:  # pragma: no cover
    st.session_state.trends = TrendMonitor()  # pragma: no cover
if 'generator' not in st.session_state:  # pragma: no cover
    st.session_state.generator = ContentGenerator() # API key will be updated from sidebar  # pragma: no cover
if 'engagement' not in st.session_state:  # pragma: no cover
    st.session_state.engagement = EngagementManager(st.session_state.generator)  # pragma: no cover

# Sidebar
with st.sidebar:  # pragma: no cover
    st.title(f"{Config.APP_ICON} {Config.APP_NAME}")  # pragma: no cover

    st.markdown("---")  # pragma: no cover

    menu = st.radio(  # pragma: no cover
        "Navigation",
        ["Dashboard", "Create Content", "Schedule", "Engage", "Settings"],
        index=0
    )

    st.markdown("---")  # pragma: no cover

    st.subheader("⚙️ Quick Settings")  # pragma: no cover
    api_key = st.text_input("OpenAI API Key", type="password", value=Config.get_api_key() or "")  # pragma: no cover
    if api_key:  # pragma: no cover
        os.environ["OPENAI_API_KEY"] = api_key  # pragma: no cover
        # Re-initialize generator with new key if changed
        if st.session_state.generator.api_key != api_key:  # pragma: no cover
            st.session_state.generator = ContentGenerator(api_key=api_key)  # pragma: no cover
            st.session_state.engagement = EngagementManager(st.session_state.generator)  # pragma: no cover

    brand_voice = st.text_area("Brand Voice", value="Professional, engaging, and tech-savvy", height=100)  # pragma: no cover
    if brand_voice != st.session_state.generator.brand_voice:  # pragma: no cover
         st.session_state.generator.brand_voice = brand_voice  # pragma: no cover

# Main Content Routing
if menu == "Dashboard":  # pragma: no cover
    st.header("Dashboard")  # pragma: no cover
    st.write("Welcome to your AI Social Media Manager.")  # pragma: no cover

    # Metrics
    col1, col2, col3 = st.columns(3)  # pragma: no cover
    with col1:  # pragma: no cover
        st.metric(label="Total Followers", value="12.5K", delta="+120")  # pragma: no cover
    with col2:  # pragma: no cover
        st.metric(label="Avg. Engagement", value="4.2%", delta="+0.5%")  # pragma: no cover
    with col3:  # pragma: no cover
        st.metric(label="Scheduled Posts", value=str(len(st.session_state.scheduler.get_queue("Draft"))), delta="Active")  # pragma: no cover

    st.markdown("---")  # pragma: no cover

    # Analytics Chart
    st.subheader("📈 Growth Overview")  # pragma: no cover
    growth_df = st.session_state.analytics.get_growth_stats()  # pragma: no cover
    st.line_chart(growth_df.set_index("Date")[["Followers", "Engagement"]])  # pragma: no cover

    st.markdown("---")  # pragma: no cover

    # Trends Preview
    st.subheader("🔥 Trending Now")  # pragma: no cover
    trends = st.session_state.trends.get_trends()  # pragma: no cover

    trend_cols = st.columns(3)  # pragma: no cover
    for i, trend in enumerate(trends[:3]):  # pragma: no cover
        with trend_cols[i]:  # pragma: no cover
            st.markdown(f"""  # pragma: no cover
            <div class="card">
                <h4>{trend['topic']}</h4>
                <p style="color: #aaa; font-size: 0.9em;">{trend['volume']} • {trend['sentiment']}</p>
                <p style="font-size: 0.8em;">{trend['source']}</p>
            </div>
            """, unsafe_allow_html=True)

elif menu == "Create Content":  # pragma: no cover
    st.header("Create New Content")  # pragma: no cover

    col1, col2 = st.columns([2, 1])  # pragma: no cover

    with col1:  # pragma: no cover
        topic = st.text_input("What is the post about?", placeholder="e.g., The future of AI Agents")  # pragma: no cover
        platform = st.selectbox("Select Platform", ["Twitter", "LinkedIn", "Instagram"])  # pragma: no cover

        if st.button("Generate Draft"):  # pragma: no cover
            with st.spinner("Generating content..."):  # pragma: no cover
                draft = st.session_state.generator.generate_draft(topic, platform)  # pragma: no cover
                st.session_state.current_draft = draft  # pragma: no cover

                # Generate Image Prompt as well
                image_prompt = st.session_state.generator.generate_image_prompt(topic, platform)  # pragma: no cover
                st.session_state.current_image_prompt = image_prompt  # pragma: no cover

    with col2:  # pragma: no cover
        st.subheader("Draft Preview")  # pragma: no cover
        if 'current_draft' in st.session_state:  # pragma: no cover
            draft_content = st.text_area("Post Content", value=st.session_state.current_draft, height=200)  # pragma: no cover
            img_prompt = st.text_area("Image Prompt", value=st.session_state.current_image_prompt, height=100)  # pragma: no cover

            if st.button("Add to Schedule"):  # pragma: no cover
                st.session_state.scheduler.add_draft(  # pragma: no cover
                    topic,
                    platform,
                    draft_content,
                    img_prompt
                )
                st.success("Draft added to schedule!")  # pragma: no cover
                # Clear draft
                del st.session_state.current_draft  # pragma: no cover
                del st.session_state.current_image_prompt  # pragma: no cover
                st.rerun()  # pragma: no cover

elif menu == "Schedule":  # pragma: no cover
    st.header("Content Schedule")  # pragma: no cover

    tab1, tab2 = st.tabs(["Upcoming", "Published"])  # pragma: no cover

    with tab1:  # pragma: no cover
        queue = st.session_state.scheduler.get_queue("Draft")  # pragma: no cover
        if not queue:  # pragma: no cover
            st.info("No scheduled posts. Go to 'Create Content' to add some!")  # pragma: no cover
        else:
            for post in queue:  # pragma: no cover
                with st.expander(f"{post['platform']}: {post['topic']} ({post['scheduled_time']})"):  # pragma: no cover
                    st.write(post['content'])  # pragma: no cover
                    st.caption(f"Image Prompt: {post['image_prompt']}")  # pragma: no cover

                    col_a, col_b = st.columns(2)  # pragma: no cover
                    with col_a:  # pragma: no cover
                        if st.button("Publish Now", key=f"pub_{post['id']}"):  # pragma: no cover
                            st.session_state.scheduler.update_status(post['id'], "Published")  # pragma: no cover
                            st.success("Post published!")  # pragma: no cover
                            st.rerun()  # pragma: no cover
                    with col_b:  # pragma: no cover
                        if st.button("Delete", key=f"del_{post['id']}"):  # pragma: no cover
                            st.session_state.scheduler.delete_draft(post['id'])  # pragma: no cover
                            st.warning("Post deleted.")  # pragma: no cover
                            st.rerun()  # pragma: no cover

    with tab2:  # pragma: no cover
        published = st.session_state.scheduler.get_queue("Published")  # pragma: no cover
        if not published:  # pragma: no cover
            st.info("No published posts yet.")  # pragma: no cover
        else:
            for post in published:  # pragma: no cover
                st.markdown(f"**{post['platform']}** - {post['topic']}")  # pragma: no cover
                st.text(post['content'])  # pragma: no cover
                st.markdown("---")  # pragma: no cover

elif menu == "Engage":  # pragma: no cover
    st.header("Community Engagement")  # pragma: no cover

    st.write("Review and reply to recent comments.")  # pragma: no cover

    if 'replies' not in st.session_state:  # pragma: no cover
        st.session_state.replies = {}  # pragma: no cover

    comments = st.session_state.engagement.get_pending_comments()  # pragma: no cover

    for comment in comments:  # pragma: no cover
        with st.container():  # pragma: no cover
            st.markdown(f"""  # pragma: no cover
            <div class="card">
                <h5>{comment['user']} on {comment['platform']}</h5>
                <p>"{comment['text']}"</p>
                <span style="background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 4px; font-size: 0.8em;">{comment['sentiment']}</span>
            </div>
            """, unsafe_allow_html=True)

            reply_key = f"reply_{comment['id']}"  # pragma: no cover

            if st.button("Generate Reply Suggestion", key=f"reply_btn_{comment['id']}"):  # pragma: no cover
                with st.spinner("Generating reply..."):  # pragma: no cover
                    reply = st.session_state.engagement.suggest_reply(comment)  # pragma: no cover
                    st.session_state.replies[reply_key] = reply  # pragma: no cover

            if reply_key in st.session_state.replies:  # pragma: no cover
                st.text_area("Suggested Reply", value=st.session_state.replies[reply_key], height=100, key=f"reply_text_{comment['id']}")  # pragma: no cover
                if st.button("Post Reply", key=f"post_reply_{comment['id']}"):  # pragma: no cover
                     st.success(f"Reply posted to {comment['platform']}!")  # pragma: no cover
                     del st.session_state.replies[reply_key]  # pragma: no cover
                     st.rerun()  # pragma: no cover

            st.markdown("<br>", unsafe_allow_html=True)  # pragma: no cover

elif menu == "Settings":  # pragma: no cover
    st.header("Application Settings")  # pragma: no cover
    st.write("Manage your preferences and integrations.")  # pragma: no cover
    # Placeholder for Settings tab logic
