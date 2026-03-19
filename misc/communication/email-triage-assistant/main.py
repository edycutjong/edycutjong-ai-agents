import streamlit as st
import datetime
from agent.email_service import get_email_provider
from agent.llm_service import LLMService
from agent.models import Email, TriageResult
from config import Config

# --- Page Configuration ---
st.set_page_config(
    page_title="Email Triage Assistant",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS / Premium UI ---
def load_css():
    st.markdown("""
        <style>
        /* Modern Font Import */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Gradient Background for Header */
        .stAppHeader {
            background: linear-gradient(90deg, #4C1D95 0%, #8B5CF6 100%);
            color: white;
        }

        /* Card Styling for Emails */
        .email-card {
            background-color: #f8fafc;
            border-left: 4px solid #cbd5e1;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .email-card:hover {
            background-color: #f1f5f9;
            transform: translateX(2px);
        }
        .email-card.selected {
            background-color: #eff6ff;
            border-left-color: #3b82f6;
        }
        .email-card.urgent {
            border-left-color: #ef4444;
        }
        .email-card.newsletter {
            border-left-color: #10b981;
        }

        /* Metric Cards */
        div[data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #1e293b;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #f8fafc;
        }

        /* Button Styling */
        .stButton button {
            background-color: #4f46e5;
            color: white;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            border: none;
            font-weight: 600;
        }
        .stButton button:hover {
            background-color: #4338ca;
        }
        </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if "provider" not in st.session_state:
    st.session_state.provider = get_email_provider(use_mock=True) # Default to Mock for safety/demo
if "llm_service" not in st.session_state:
    st.session_state.llm_service = LLMService()
if "emails" not in st.session_state:
    with st.spinner("Connecting to email server..."):
        try:
            st.session_state.provider.connect()
            st.session_state.emails = st.session_state.provider.fetch_emails(limit=10)
        except Exception as e:  # pragma: no cover
            st.error(f"Failed to connect: {e}")  # pragma: no cover
            st.session_state.emails = []  # pragma: no cover
if "selected_email" not in st.session_state:
    st.session_state.selected_email = None
if "triage_results" not in st.session_state:
    st.session_state.triage_results = {}
if "briefing" not in st.session_state:
    st.session_state.briefing = None

# --- Helper Functions ---
def triage_email(email: Email):
    if email.id not in st.session_state.triage_results:  # pragma: no cover
        with st.spinner(f"Analyzing email: {email.subject[:30]}..."):  # pragma: no cover
            result = st.session_state.llm_service.analyze_email(email)  # pragma: no cover
            st.session_state.triage_results[email.id] = result  # pragma: no cover
    return st.session_state.triage_results[email.id]  # pragma: no cover

def get_briefing():
    if not st.session_state.briefing:
        with st.spinner("Generating Daily Briefing..."):
            # Filter for urgent/important emails if possible, or just send top 5
            top_emails = st.session_state.emails[:5]
            st.session_state.briefing = st.session_state.llm_service.generate_briefing(top_emails)
    return st.session_state.briefing

# --- Main UI Layout ---
def main():
    load_css()

    # Header
    st.title("📧 Email Triage Assistant")

    # Daily Briefing Section (Collapsible)
    with st.expander("Daily Briefing", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(get_briefing())
        with col2:
            urgent_count = sum(1 for e in st.session_state.emails if "urgent" in e.subject.lower())
            st.metric("Total Emails", len(st.session_state.emails))
            st.metric("Urgent Items", urgent_count)

    st.markdown("---")

    # Split View
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.subheader("Inbox")

        # Filter/Search (Visual only for now)
        search_query = st.text_input("Search emails...", "")

        for email in st.session_state.emails:
            if search_query and search_query.lower() not in email.subject.lower():
                continue  # pragma: no cover

            # Determine card class based on simple heuristic or triage result if available
            card_class = "email-card"
            if st.session_state.selected_email and st.session_state.selected_email.id == email.id:
                card_class += " selected"  # pragma: no cover

            # Use triage result if available for color coding
            category = "Unprocessed"
            if email.id in st.session_state.triage_results:
                triage = st.session_state.triage_results[email.id]  # pragma: no cover
                category = triage.category  # pragma: no cover
                if triage.category == "Urgent":  # pragma: no cover
                    card_class += " urgent"  # pragma: no cover
                elif triage.category == "Newsletter":  # pragma: no cover
                    card_class += " newsletter"  # pragma: no cover

            # Render Card
            # We use a button that looks like a card via CSS
            # Using st.button might be tricky for custom styling, so we use a container with a button inside or clickable div?
            # Streamlit buttons are limited. Let's use st.button with key.

            with st.container(border=True):
                col_a, col_b = st.columns([0.8, 0.2])
                with col_a:
                    st.markdown(f"**{email.sender}**")
                    st.caption(f"{email.subject[:40]}...")
                with col_b:
                    if st.button("View", key=f"btn_{email.id}"):
                        st.session_state.selected_email = email  # pragma: no cover
                        # Trigger triage on selection
                        triage_email(email)  # pragma: no cover
                        st.rerun()  # pragma: no cover

    with right_col:
        if st.session_state.selected_email:
            email = st.session_state.selected_email  # pragma: no cover
            triage = st.session_state.triage_results.get(email.id)  # pragma: no cover

            st.header(email.subject)  # pragma: no cover
            st.markdown(f"**From:** {email.sender} | **Date:** {email.date.strftime('%Y-%m-%d %H:%M')}")  # pragma: no cover

            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📧 Content", "🤖 AI Analysis", "✍️ Draft Reply"])  # pragma: no cover

            with tab1:  # pragma: no cover
                st.markdown(email.body)  # pragma: no cover

            with tab2:  # pragma: no cover
                if triage:  # pragma: no cover
                    st.subheader(f"Category: {triage.category}")  # pragma: no cover
                    st.progress(triage.urgency_score / 10, text=f"Urgency Score: {triage.urgency_score}/10")  # pragma: no cover

                    st.info(f"**Summary:** {triage.summary}")  # pragma: no cover

                    if triage.action_items:  # pragma: no cover
                        st.write("### Action Items")  # pragma: no cover
                        for item in triage.action_items:  # pragma: no cover
                            st.checkbox(item, key=f"action_{email.id}_{item}")  # pragma: no cover

                    if triage.suggested_actions:  # pragma: no cover
                        st.write("### Suggested Actions")  # pragma: no cover
                        for action in triage.suggested_actions:  # pragma: no cover
                            st.markdown(f"- {action}")  # pragma: no cover
                else:
                    st.warning("Analysis pending...")  # pragma: no cover

            with tab3:  # pragma: no cover
                st.write("### Draft a Reply")  # pragma: no cover
                col_tone, col_instr = st.columns([1, 2])  # pragma: no cover
                with col_tone:  # pragma: no cover
                    tone = st.selectbox("Tone", ["Professional", "Casual", "Direct", "Empathetic"], index=0)  # pragma: no cover
                with col_instr:  # pragma: no cover
                    instructions = st.text_input("Special Instructions", placeholder="e.g., Decline politely")  # pragma: no cover

                if st.button("Generate Draft"):  # pragma: no cover
                    with st.spinner("Drafting reply..."):  # pragma: no cover
                        draft = st.session_state.llm_service.draft_reply(email, instructions, tone)  # pragma: no cover
                        st.session_state[f"draft_{email.id}"] = draft  # pragma: no cover

                if f"draft_{email.id}" in st.session_state:  # pragma: no cover
                    st.text_area("Draft Body", value=st.session_state[f"draft_{email.id}"], height=200)  # pragma: no cover
                    col_copy, col_send = st.columns(2)  # pragma: no cover
                    with col_copy:  # pragma: no cover
                        st.button("Copy to Clipboard") # Placeholder  # pragma: no cover
                    with col_send:  # pragma: no cover
                        st.button("Send Reply", type="primary") # Placeholder  # pragma: no cover

        else:
            st.info("Select an email from the inbox to view details.")

if __name__ == "__main__":
    main()
