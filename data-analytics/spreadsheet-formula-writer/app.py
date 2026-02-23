import streamlit as st
import sys
import os
from pathlib import Path
import logging

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))

try:
    from agent.core import FormulaWriterAgent
    from agent.models import FormulaResponse
except ImportError:
    st.error("Could not import agent modules. Please run from the project root.")
    st.stop()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Spreadsheet Formula Writer",
    page_icon="📊",
    layout="wide"
)

def display_result(response: FormulaResponse, target: str):
    """Display the formula response components."""

    st.markdown(f"### **Generated Formula ({target})**")
    st.code(response.formula, language="vb")

    st.markdown("### **Explanation**")
    st.markdown(response.explanation)

    if response.alternatives or response.examples:
        col1, col2 = st.columns(2)

        with col1:
            if response.alternatives:
                st.markdown("#### Alternatives")
                for alt in response.alternatives:
                    st.info(alt)

        with col2:
            if response.examples:
                st.markdown("#### Usage Examples")
                for ex in response.examples:
                    # Try to format markdown tables if present
                    st.markdown(ex)

def main():
    st.title("📊 Spreadsheet Formula Writer")
    st.markdown("Convert natural language questions into complex Excel/Google Sheets formulas.")

    # Sidebar
    with st.sidebar:
        st.header("Configuration")

        # Check for API Key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = st.text_input("OpenAI API Key", type="password", help="Required if not set in environment variables.")
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key

        target_app = st.selectbox(
            "Target Application",
            ["Excel", "Google Sheets"],
            index=0
        )

        model_name = st.selectbox(
            "Model",
            ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            index=0
        )

        st.divider()
        st.markdown("### Capabilities")
        st.markdown("""
        - **Complex Logic**: Nested IFs, LOOKUPs
        - **Modern Functions**: LAMBDA, LET, XLOOKUP
        - **Array Formulas**: SPILL ranges, dynamic arrays
        - **Explanations**: Step-by-step logic breakdown
        """)

    # Main Area
    query = st.text_area(
        "Describe the formula you need:",
        height=150,
        placeholder="e.g., 'Look up the value in column A from Sheet1, match it with column B in Sheet2, and return the sum of column C if the date in column D is from last month.'"
    )

    if st.button("Generate Formula", type="primary"):
        if not query:
            st.warning("Please enter a query description.")
            return

        if not os.getenv("OPENAI_API_KEY"):
            st.error("Please provide an OpenAI API Key in the sidebar.")
            return

        with st.spinner(f"Generating {target_app} formula using {model_name}..."):
            try:
                agent = FormulaWriterAgent(model_name=model_name)
                response = agent.generate_formula(query, target_application=target_app)

                # Store in history
                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.insert(0, {
                    "query": query,
                    "response": response,
                    "target": target_app
                })

                # Display current result immediately
                st.success("Success!")
                display_result(response, target_app)

            except Exception as e:
                st.error(f"Error: {str(e)}")

    # History Section
    if "history" in st.session_state and st.session_state.history:
        st.divider()
        st.subheader("History")

        for i, item in enumerate(st.session_state.history):
            # Skip the first one if it's the one currently displayed?
            # Actually, showing history below is fine even if duplicate of top.
            # To avoid clutter, maybe we only show history items excluding the current one if we just generated it?
            # But simpler to just show all.

            with st.expander(f"{item['target']}: {item['query'][:80]}..." + (" (Latest)" if i == 0 else ""), expanded=False):
                display_result(item['response'], item['target'])

if __name__ == "__main__":
    main()
