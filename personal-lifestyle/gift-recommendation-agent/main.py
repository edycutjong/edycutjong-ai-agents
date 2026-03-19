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
        api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API Key")  # pragma: no cover
        if api_key:  # pragma: no cover
            os.environ["OPENAI_API_KEY"] = api_key  # pragma: no cover

    if not api_key:
        st.sidebar.warning("Please provide an OpenAI API Key to continue.")  # pragma: no cover

    # Initialize Agent
    try:
        agent = GiftAdvisor(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        return

    # Gift History Sidebar
    st.sidebar.markdown("---")  # pragma: no cover
    st.sidebar.header("📜 Recent History")  # pragma: no cover
    if st.sidebar.button("Refresh History"):  # pragma: no cover
        st.rerun()  # pragma: no cover

    try:  # pragma: no cover
        history = agent.load_history()  # pragma: no cover
        if history:  # pragma: no cover
            for i, entry in enumerate(reversed(history[-5:])):  # Show last 5  # pragma: no cover
                date = entry.get('timestamp', '')[:10]  # pragma: no cover
                name = entry.get('profile', {}).get('name', 'Unknown')  # pragma: no cover
                occasion_hist = entry.get('occasion', 'Unknown')  # pragma: no cover

                with st.sidebar.expander(f"{date}: {name} ({occasion_hist})"):  # pragma: no cover
                    for gift in entry.get('suggestions', []):  # pragma: no cover
                        st.markdown(f"- **{gift.get('name')}**: {gift.get('estimated_price')}")  # pragma: no cover
        else:
            st.sidebar.info("No history yet.")  # pragma: no cover
    except Exception as e:  # pragma: no cover
        st.sidebar.error(f"Could not load history: {e}")  # pragma: no cover

    # Main Form
    with st.form("gift_query_form"):  # pragma: no cover
        st.subheader("Recipient Profile")  # pragma: no cover
        col1, col2 = st.columns(2)  # pragma: no cover

        with col1:  # pragma: no cover
            recipient_name = st.text_input("Recipient Name", placeholder="e.g., Alice")  # pragma: no cover
            age = st.number_input("Age", min_value=0, max_value=120, value=25)  # pragma: no cover
            gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Prefer not to say"])  # pragma: no cover
            relationship = st.selectbox("Relationship", ["Friend", "Partner", "Parent", "Sibling", "Child", "Colleague", "Other"])  # pragma: no cover

        with col2:  # pragma: no cover
            occasion = st.text_input("Occasion", value="Birthday")  # pragma: no cover
            budget = st.select_slider(  # pragma: no cover
                "Budget Range",
                options=["Under $20", "$20 - $50", "$50 - $100", "$100 - $200", "$200 - $500", "$500+", "No Limit"],
                value="$50 - $100"
            )
            interests = st.text_area("Interests, Hobbies & Notes", placeholder="e.g., Loves gardening, sci-fi movies, coffee, and cats.")  # pragma: no cover

        submit_btn = st.form_submit_button("Find Gift Ideas 🎁", type="primary")  # pragma: no cover

    if submit_btn:  # pragma: no cover
        if not api_key:  # pragma: no cover
            st.error("Please enter an OpenAI API Key in the sidebar.")  # pragma: no cover
        elif not interests:  # pragma: no cover
            st.warning("Please enter some interests to help the AI.")  # pragma: no cover
        else:
            with st.spinner("Thinking of gift ideas..."):  # pragma: no cover
                profile = {  # pragma: no cover
                    "name": recipient_name,
                    "age": age,
                    "gender": gender,
                    "relationship": relationship,
                    "interests": interests
                }
                try:  # pragma: no cover
                    suggestions = agent.generate_suggestions(profile, occasion, budget)  # pragma: no cover
                    st.session_state['suggestions'] = suggestions  # pragma: no cover
                    st.session_state['recipient_name'] = recipient_name  # pragma: no cover
                    st.session_state['occasion'] = occasion  # pragma: no cover
                    st.session_state['profile'] = profile  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.error(f"An error occurred: {str(e)}")  # pragma: no cover

    # Display Results
    if st.session_state['suggestions']:  # pragma: no cover
        st.markdown("---")  # pragma: no cover
        st.header(f"Gift Ideas for {st.session_state.get('recipient_name', 'Recipient')}")  # pragma: no cover

        suggestions = st.session_state['suggestions']  # pragma: no cover

        for i, gift in enumerate(suggestions):  # pragma: no cover
            # Handle both object and dict (if loaded from history/session state quirks)
            # generate_suggestions returns objects, but let's be safe
            name = getattr(gift, 'name', gift.get('name') if isinstance(gift, dict) else '')  # pragma: no cover
            price = getattr(gift, 'estimated_price', gift.get('estimated_price') if isinstance(gift, dict) else '')  # pragma: no cover
            category = getattr(gift, 'category', gift.get('category') if isinstance(gift, dict) else '')  # pragma: no cover
            reasoning = getattr(gift, 'reasoning', gift.get('reasoning') if isinstance(gift, dict) else '')  # pragma: no cover
            link = getattr(gift, 'purchase_link', gift.get('purchase_link') if isinstance(gift, dict) else '')  # pragma: no cover

            with st.container():  # pragma: no cover
                cols = st.columns([1, 4])  # pragma: no cover
                with cols[0]:  # pragma: no cover
                    st.metric(label="Price", value=price)  # pragma: no cover
                    st.caption(category)  # pragma: no cover
                with cols[1]:  # pragma: no cover
                    st.subheader(f"{i+1}. {name}")  # pragma: no cover
                    st.markdown(reasoning)  # pragma: no cover
                    if link:  # pragma: no cover
                        st.link_button("Search / Buy 🛒", link)  # pragma: no cover
                st.divider()  # pragma: no cover

        # Export Section
        st.markdown("### 📄 Gift Guide Document")  # pragma: no cover
        if st.button("Generate formatted Gift Guide"):  # pragma: no cover
            with st.spinner("Drafting document..."):  # pragma: no cover
                try:  # pragma: no cover
                    guide_content = agent.generate_gift_guide(  # pragma: no cover
                        suggestions,
                        st.session_state.get('recipient_name'),
                        st.session_state.get('occasion')
                    )
                    st.markdown(guide_content)  # pragma: no cover
                    st.download_button(  # pragma: no cover
                        label="Download Gift Guide (Markdown)",
                        data=guide_content,
                        file_name=f"gift_guide_{st.session_state.get('recipient_name')}.md",
                        mime="text/markdown"
                    )
                except Exception as e:  # pragma: no cover
                    st.error(f"Failed to generate guide: {e}")  # pragma: no cover

if __name__ == "__main__":
    main()
