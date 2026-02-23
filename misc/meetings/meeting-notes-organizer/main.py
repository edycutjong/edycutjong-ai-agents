import streamlit as st
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from config import Config
from agent.processor import MeetingProcessor
from agent.storage import MeetingStorage
from agent.integrations import create_jira_issue, create_calendar_event

st.set_page_config(
    page_title="Meeting Notes Organizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open(os.path.join(os.path.dirname(__file__), "style.css")) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("📝 Meeting Notes Organizer")

# Sidebar
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", value=Config.OPENAI_API_KEY or "", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    st.divider()
    page = st.radio("Navigation", ["New Meeting", "Archive"])

storage = MeetingStorage()

if page == "New Meeting":
    st.header("New Meeting Transcript")
    transcript = st.text_area("Paste transcript here...", height=300)

    if st.button("Process Meeting", type="primary"):
        if not transcript:
            st.error("Please enter a transcript.")
        elif not api_key and not Config.OPENAI_API_KEY:
            st.error("Please provide an OpenAI API Key.")
        else:
            with st.spinner("Processing meeting transcript..."):
                processor = MeetingProcessor(api_key=api_key or Config.OPENAI_API_KEY)
                result = processor.process_transcript(transcript)

                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    # Save to storage
                    meeting_id = storage.save_meeting(
                        transcript,
                        result["summary"],
                        result["action_items"],
                        result["email_draft"]
                    )
                    st.success("Meeting processed and saved!")

                    # Store in session state to display
                    st.session_state.current_meeting = result
                    st.session_state.current_meeting_id = meeting_id

    if "current_meeting" in st.session_state:
        result = st.session_state.current_meeting

        tab1, tab2, tab3 = st.tabs(["Summary", "Action Items", "Email Draft"])

        with tab1:
            st.markdown(result["summary"])

        with tab2:
            st.subheader("Action Items")
            if not result["action_items"]:
                st.info("No action items extracted.")
            else:
                for idx, item in enumerate(result["action_items"]):
                    with st.expander(f"{item.get('priority', 'Medium')} Priority: {item.get('task')}"):
                        st.write(f"**Assignee:** {item.get('assignee')}")
                        st.write(f"**Due Date:** {item.get('due_date')}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Create Jira Issue", key=f"jira_{idx}_{st.session_state.get('current_meeting_id', 'new')}"):
                                 res = create_jira_issue(item.get('task'), f"Assigned to {item.get('assignee')}")
                                 st.success(res['message'])
                        with col2:
                            if st.button("Add to Calendar", key=f"cal_{idx}_{st.session_state.get('current_meeting_id', 'new')}"):
                                 res = create_calendar_event(item.get('task'), "Tomorrow", "Meeting follow-up")
                                 st.success(res['message'])

        with tab3:
            st.text_area("Draft Email", value=result["email_draft"], height=300)

elif page == "Archive":
    st.header("Meeting Archive")

    search_query = st.text_input("Search meetings...", placeholder="Search by keyword, task, or summary")

    if search_query:
        meetings = storage.search_meetings(search_query)
    else:
        meetings = storage.get_all_meetings()

    if not meetings:
        st.info("No meetings found.")
    else:
        for m in meetings:
            date_str = datetime.fromisoformat(m["timestamp"]).strftime("%Y-%m-%d %H:%M")
            summary_preview = m['summary'].split('\n')[0][:100] if m['summary'] else "No Summary"
            with st.expander(f"{date_str} - {summary_preview}..."):
                st.markdown("### Summary")
                st.markdown(m["summary"])

                st.markdown("### Action Items")
                for item in m["action_items"]:
                    st.write(f"- **{item.get('task')}** ({item.get('assignee')})")

                st.markdown("### Email Draft")
                st.text_area("Email", m["email_draft"], key=f"email_{m['id']}", height=100, disabled=True)
