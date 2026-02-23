import streamlit as st
import os
import json
import sys

# Add project root to path if needed (for relative imports when running from different location)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.gift_advisor import GiftAdvisor

st.set_page_config(
    page_title="Gift Recommendation Agent",
    page_icon="🎁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'suggestions' not in st.session_state:
    st.session_state['suggestions'] = None

def main():
    st.title("🎁 Personalized Gift Recommendation Agent")
    st.markdown("### Find the perfect gift with AI-powered suggestions")

    # Sidebar
    st.sidebar.header("Configuration")

    # API Key Handling
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API Key")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

    if not api_key:
        st.sidebar.warning("Please provide an OpenAI API Key to continue.")

    # Initialize Agent
    try:
        agent = GiftAdvisor(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        return

    # Gift History Sidebar
    st.sidebar.markdown("---")
    st.sidebar.header("📜 Recent History")
    if st.sidebar.button("Refresh History"):
        st.rerun()

    try:
        history = agent.load_history()
        if history:
            for i, entry in enumerate(reversed(history[-5:])):  # Show last 5
                date = entry.get('timestamp', '')[:10]
                name = entry.get('profile', {}).get('name', 'Unknown')
                occasion_hist = entry.get('occasion', 'Unknown')

                with st.sidebar.expander(f"{date}: {name} ({occasion_hist})"):
                    for gift in entry.get('suggestions', []):
                        st.markdown(f"- **{gift.get('name')}**: {gift.get('estimated_price')}")
        else:
            st.sidebar.info("No history yet.")
    except Exception as e:
        st.sidebar.error(f"Could not load history: {e}")

    # Main Form
    with st.form("gift_query_form"):
        st.subheader("Recipient Profile")
        col1, col2 = st.columns(2)

        with col1:
            recipient_name = st.text_input("Recipient Name", placeholder="e.g., Alice")
            age = st.number_input("Age", min_value=0, max_value=120, value=25)
            gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Prefer not to say"])
            relationship = st.selectbox("Relationship", ["Friend", "Partner", "Parent", "Sibling", "Child", "Colleague", "Other"])

        with col2:
            occasion = st.text_input("Occasion", value="Birthday")
            budget = st.select_slider(
                "Budget Range",
                options=["Under $20", "$20 - $50", "$50 - $100", "$100 - $200", "$200 - $500", "$500+", "No Limit"],
                value="$50 - $100"
            )
            interests = st.text_area("Interests, Hobbies & Notes", placeholder="e.g., Loves gardening, sci-fi movies, coffee, and cats.")

        submit_btn = st.form_submit_button("Find Gift Ideas 🎁", type="primary")

    if submit_btn:
        if not api_key:
            st.error("Please enter an OpenAI API Key in the sidebar.")
        elif not interests:
            st.warning("Please enter some interests to help the AI.")
        else:
            with st.spinner("Thinking of gift ideas..."):
                profile = {
                    "name": recipient_name,
                    "age": age,
                    "gender": gender,
                    "relationship": relationship,
                    "interests": interests
                }
                try:
                    suggestions = agent.generate_suggestions(profile, occasion, budget)
                    st.session_state['suggestions'] = suggestions
                    st.session_state['recipient_name'] = recipient_name
                    st.session_state['occasion'] = occasion
                    st.session_state['profile'] = profile
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    # Display Results
    if st.session_state['suggestions']:
        st.markdown("---")
        st.header(f"Gift Ideas for {st.session_state.get('recipient_name', 'Recipient')}")

        suggestions = st.session_state['suggestions']

        for i, gift in enumerate(suggestions):
            # Handle both object and dict (if loaded from history/session state quirks)
            # generate_suggestions returns objects, but let's be safe
            name = getattr(gift, 'name', gift.get('name') if isinstance(gift, dict) else '')
            price = getattr(gift, 'estimated_price', gift.get('estimated_price') if isinstance(gift, dict) else '')
            category = getattr(gift, 'category', gift.get('category') if isinstance(gift, dict) else '')
            reasoning = getattr(gift, 'reasoning', gift.get('reasoning') if isinstance(gift, dict) else '')
            link = getattr(gift, 'purchase_link', gift.get('purchase_link') if isinstance(gift, dict) else '')

            with st.container():
                cols = st.columns([1, 4])
                with cols[0]:
                    st.metric(label="Price", value=price)
                    st.caption(category)
                with cols[1]:
                    st.subheader(f"{i+1}. {name}")
                    st.markdown(reasoning)
                    if link:
                        st.link_button("Search / Buy 🛒", link)
                st.divider()

        # Export Section
        st.markdown("### 📄 Gift Guide Document")
        if st.button("Generate formatted Gift Guide"):
            with st.spinner("Drafting document..."):
                try:
                    guide_content = agent.generate_gift_guide(
                        suggestions,
                        st.session_state.get('recipient_name'),
                        st.session_state.get('occasion')
                    )
                    st.markdown(guide_content)
                    st.download_button(
                        label="Download Gift Guide (Markdown)",
                        data=guide_content,
                        file_name=f"gift_guide_{st.session_state.get('recipient_name')}.md",
                        mime="text/markdown"
                    )
                except Exception as e:
                    st.error(f"Failed to generate guide: {e}")

if __name__ == "__main__":
    main()
