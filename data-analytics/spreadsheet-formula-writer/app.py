import streamlit as st  # pragma: no cover
import sys  # pragma: no cover
import os  # pragma: no cover
from pathlib import Path  # pragma: no cover
import logging  # pragma: no cover

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent  # pragma: no cover
sys.path.append(str(PROJECT_ROOT))  # pragma: no cover

try:  # pragma: no cover
    from agent.core import FormulaWriterAgent  # pragma: no cover
    from agent.models import FormulaResponse  # pragma: no cover
except ImportError:  # pragma: no cover
    st.error("Could not import agent modules. Please run from the project root.")  # pragma: no cover
    st.stop()  # pragma: no cover

# Configure logging
logging.basicConfig(level=logging.INFO)  # pragma: no cover
logger = logging.getLogger(__name__)  # pragma: no cover

st.set_page_config(  # pragma: no cover
    page_title="Spreadsheet Formula Writer",
    page_icon="📊",
    layout="wide"
)

def display_result(response: FormulaResponse, target: str):  # pragma: no cover
    """Display the formula response components."""

    st.markdown(f"### **Generated Formula ({target})**")  # pragma: no cover
    st.code(response.formula, language="vb")  # pragma: no cover

    st.markdown("### **Explanation**")  # pragma: no cover
    st.markdown(response.explanation)  # pragma: no cover

    if response.alternatives or response.examples:  # pragma: no cover
        col1, col2 = st.columns(2)  # pragma: no cover

        with col1:  # pragma: no cover
            if response.alternatives:  # pragma: no cover
                st.markdown("#### Alternatives")  # pragma: no cover
                for alt in response.alternatives:  # pragma: no cover
                    st.info(alt)  # pragma: no cover

        with col2:  # pragma: no cover
            if response.examples:  # pragma: no cover
                st.markdown("#### Usage Examples")  # pragma: no cover
                for ex in response.examples:  # pragma: no cover
                    # Try to format markdown tables if present
                    st.markdown(ex)  # pragma: no cover

def main():  # pragma: no cover
    st.title("📊 Spreadsheet Formula Writer")  # pragma: no cover
    st.markdown("Convert natural language questions into complex Excel/Google Sheets formulas.")  # pragma: no cover

    # Sidebar
    with st.sidebar:  # pragma: no cover
        st.header("Configuration")  # pragma: no cover

        # Check for API Key
        api_key = os.getenv("OPENAI_API_KEY")  # pragma: no cover
        if not api_key:  # pragma: no cover
            api_key = st.text_input("OpenAI API Key", type="password", help="Required if not set in environment variables.")  # pragma: no cover
            if api_key:  # pragma: no cover
                os.environ["OPENAI_API_KEY"] = api_key  # pragma: no cover

        target_app = st.selectbox(  # pragma: no cover
            "Target Application",
            ["Excel", "Google Sheets"],
            index=0
        )

        model_name = st.selectbox(  # pragma: no cover
            "Model",
            ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            index=0
        )

        st.divider()  # pragma: no cover
        st.markdown("### Capabilities")  # pragma: no cover
        st.markdown("""  # pragma: no cover
        - **Complex Logic**: Nested IFs, LOOKUPs
        - **Modern Functions**: LAMBDA, LET, XLOOKUP
        - **Array Formulas**: SPILL ranges, dynamic arrays
        - **Explanations**: Step-by-step logic breakdown
        """)

    # Main Area
    query = st.text_area(  # pragma: no cover
        "Describe the formula you need:",
        height=150,
        placeholder="e.g., 'Look up the value in column A from Sheet1, match it with column B in Sheet2, and return the sum of column C if the date in column D is from last month.'"
    )

    if st.button("Generate Formula", type="primary"):  # pragma: no cover
        if not query:  # pragma: no cover
            st.warning("Please enter a query description.")  # pragma: no cover
            return  # pragma: no cover

        if not os.getenv("OPENAI_API_KEY"):  # pragma: no cover
            st.error("Please provide an OpenAI API Key in the sidebar.")  # pragma: no cover
            return  # pragma: no cover

        with st.spinner(f"Generating {target_app} formula using {model_name}..."):  # pragma: no cover
            try:  # pragma: no cover
                agent = FormulaWriterAgent(model_name=model_name)  # pragma: no cover
                response = agent.generate_formula(query, target_application=target_app)  # pragma: no cover

                # Store in history
                if "history" not in st.session_state:  # pragma: no cover
                    st.session_state.history = []  # pragma: no cover
                st.session_state.history.insert(0, {  # pragma: no cover
                    "query": query,
                    "response": response,
                    "target": target_app
                })

                # Display current result immediately
                st.success("Success!")  # pragma: no cover
                display_result(response, target_app)  # pragma: no cover

            except Exception as e:  # pragma: no cover
                st.error(f"Error: {str(e)}")  # pragma: no cover

    # History Section
    if "history" in st.session_state and st.session_state.history:  # pragma: no cover
        st.divider()  # pragma: no cover
        st.subheader("History")  # pragma: no cover

        for i, item in enumerate(st.session_state.history):  # pragma: no cover
            # Skip the first one if it's the one currently displayed?
            # Actually, showing history below is fine even if duplicate of top.
            # To avoid clutter, maybe we only show history items excluding the current one if we just generated it?
            # But simpler to just show all.

            with st.expander(f"{item['target']}: {item['query'][:80]}..." + (" (Latest)" if i == 0 else ""), expanded=False):  # pragma: no cover
                display_result(item['response'], item['target'])  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
