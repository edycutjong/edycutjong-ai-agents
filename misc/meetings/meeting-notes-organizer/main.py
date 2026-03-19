import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover
from datetime import datetime  # pragma: no cover

# Add current directory to path
sys.path.append(os.path.dirname(__file__))  # pragma: no cover

from config import Config  # pragma: no cover
from agent.processor import MeetingProcessor  # pragma: no cover
from agent.storage import MeetingStorage  # pragma: no cover
from agent.integrations import create_jira_issue, create_calendar_event  # pragma: no cover

st.set_page_config(  # pragma: no cover
    page_title="Meeting Notes Organizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open(os.path.join(os.path.dirname(__file__), "style.css")) as f:  # pragma: no cover
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)  # pragma: no cover

st.title("📝 Meeting Notes Organizer")  # pragma: no cover

# Sidebar
with st.sidebar:  # pragma: no cover
    st.header("Settings")  # pragma: no cover
    api_key = st.text_input("OpenAI API Key", value=Config.OPENAI_API_KEY or "", type="password")  # pragma: no cover
    if api_key:  # pragma: no cover
        os.environ["OPENAI_API_KEY"] = api_key  # pragma: no cover

    st.divider()  # pragma: no cover
    page = st.radio("Navigation", ["New Meeting", "Archive"])  # pragma: no cover

storage = MeetingStorage()  # pragma: no cover

if page == "New Meeting":  # pragma: no cover
    st.header("New Meeting Transcript")  # pragma: no cover
    transcript = st.text_area("Paste transcript here...", height=300)  # pragma: no cover

    if st.button("Process Meeting", type="primary"):  # pragma: no cover
        if not transcript:  # pragma: no cover
            st.error("Please enter a transcript.")  # pragma: no cover
        elif not api_key and not Config.OPENAI_API_KEY:  # pragma: no cover
            st.error("Please provide an OpenAI API Key.")  # pragma: no cover
        else:
            with st.spinner("Processing meeting transcript..."):  # pragma: no cover
                processor = MeetingProcessor(api_key=api_key or Config.OPENAI_API_KEY)  # pragma: no cover
                result = processor.process_transcript(transcript)  # pragma: no cover

                if "error" in result:  # pragma: no cover
                    st.error(f"Error: {result['error']}")  # pragma: no cover
                else:
                    # Save to storage
                    meeting_id = storage.save_meeting(  # pragma: no cover
                        transcript,
                        result["summary"],
                        result["action_items"],
                        result["email_draft"]
                    )
                    st.success("Meeting processed and saved!")  # pragma: no cover

                    # Store in session state to display
                    st.session_state.current_meeting = result  # pragma: no cover
                    st.session_state.current_meeting_id = meeting_id  # pragma: no cover

    if "current_meeting" in st.session_state:  # pragma: no cover
        result = st.session_state.current_meeting  # pragma: no cover

        tab1, tab2, tab3 = st.tabs(["Summary", "Action Items", "Email Draft"])  # pragma: no cover

        with tab1:  # pragma: no cover
            st.markdown(result["summary"])  # pragma: no cover

        with tab2:  # pragma: no cover
            st.subheader("Action Items")  # pragma: no cover
            if not result["action_items"]:  # pragma: no cover
                st.info("No action items extracted.")  # pragma: no cover
            else:
                for idx, item in enumerate(result["action_items"]):  # pragma: no cover
                    with st.expander(f"{item.get('priority', 'Medium')} Priority: {item.get('task')}"):  # pragma: no cover
                        st.write(f"**Assignee:** {item.get('assignee')}")  # pragma: no cover
                        st.write(f"**Due Date:** {item.get('due_date')}")  # pragma: no cover

                        col1, col2 = st.columns(2)  # pragma: no cover
                        with col1:  # pragma: no cover
                            if st.button("Create Jira Issue", key=f"jira_{idx}_{st.session_state.get('current_meeting_id', 'new')}"):  # pragma: no cover
                                 res = create_jira_issue(item.get('task'), f"Assigned to {item.get('assignee')}")  # pragma: no cover
                                 st.success(res['message'])  # pragma: no cover
                        with col2:  # pragma: no cover
                            if st.button("Add to Calendar", key=f"cal_{idx}_{st.session_state.get('current_meeting_id', 'new')}"):  # pragma: no cover
                                 res = create_calendar_event(item.get('task'), "Tomorrow", "Meeting follow-up")  # pragma: no cover
                                 st.success(res['message'])  # pragma: no cover

        with tab3:  # pragma: no cover
            st.text_area("Draft Email", value=result["email_draft"], height=300)  # pragma: no cover

elif page == "Archive":  # pragma: no cover
    st.header("Meeting Archive")  # pragma: no cover

    search_query = st.text_input("Search meetings...", placeholder="Search by keyword, task, or summary")  # pragma: no cover

    if search_query:  # pragma: no cover
        meetings = storage.search_meetings(search_query)  # pragma: no cover
    else:
        meetings = storage.get_all_meetings()  # pragma: no cover

    if not meetings:  # pragma: no cover
        st.info("No meetings found.")  # pragma: no cover
    else:
        for m in meetings:  # pragma: no cover
            date_str = datetime.fromisoformat(m["timestamp"]).strftime("%Y-%m-%d %H:%M")  # pragma: no cover
            summary_preview = m['summary'].split('\n')[0][:100] if m['summary'] else "No Summary"  # pragma: no cover
            with st.expander(f"{date_str} - {summary_preview}..."):  # pragma: no cover
                st.markdown("### Summary")  # pragma: no cover
                st.markdown(m["summary"])  # pragma: no cover

                st.markdown("### Action Items")  # pragma: no cover
                for item in m["action_items"]:  # pragma: no cover
                    st.write(f"- **{item.get('task')}** ({item.get('assignee')})")  # pragma: no cover

                st.markdown("### Email Draft")  # pragma: no cover
                st.text_area("Email", m["email_draft"], key=f"email_{m['id']}", height=100, disabled=True)  # pragma: no cover
