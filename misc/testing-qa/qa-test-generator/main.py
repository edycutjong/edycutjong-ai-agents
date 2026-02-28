import streamlit as st
import os
import sys
import pandas as pd
from datetime import datetime

# Ensure the current directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from agent.parser import UIParser
from agent.test_generator import TestGenerator
from agent.runner import TestRunner

def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        /* Global Styles */
        .stApp {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }

        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            color: #f8fafc;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1e293b;
            border-right: 1px solid #334155;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px;
            color: #94a3b8;
            font-weight: 600;
        }

        .stTabs [aria-selected="true"] {
            background-color: #3b82f6;
            color: white;
        }

        /* Custom Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.5), 0 4px 6px -2px rgba(59, 130, 246, 0.3);
            border-color: transparent;
            color: white;
        }

        /* Inputs */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: #334155;
            color: white;
            border: 1px solid #475569;
            border-radius: 6px;
        }

        /* Metric Cards */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            color: #3b82f6;
        }

        /* Success/Error Messages */
        .stSuccess {
            background-color: rgba(20, 184, 166, 0.2);
            border: 1px solid #14b8a6;
            color: #ccfbf1;
        }

        .stError {
            background-color: rgba(239, 68, 68, 0.2);
            border: 1px solid #ef4444;
            color: #fee2e2;
        }

        /* Code Blocks */
        code {
            color: #e2e8f0;
            background-color: #1e293b;
        }

    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="QA Test Generator Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    inject_custom_css()

    # Sidebar Configuration
    with st.sidebar:
        st.title("🤖 QA Agent Config")

        api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
        target_url = st.text_input("Target URL", "https://example.com")

        st.divider()
        st.markdown("### Settings")
        headless_mode = st.checkbox("Headless Mode", value=Config.HEADLESS)
        model_name = st.selectbox("Model", ["gpt-4-turbo", "gpt-3.5-turbo"], index=0)

    # Main Area
    st.title("QA Test Generator Agent")
    st.markdown("Automate your QA workflow with AI-powered test generation and execution.")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Analysis", "📝 Generation", "🚀 Execution"])

    # Initialize Session State
    if "parsed_elements" not in st.session_state:
        st.session_state.parsed_elements = []
    if "ui_structure" not in st.session_state:
        st.session_state.ui_structure = ""
    if "scenarios" not in st.session_state:
        st.session_state.scenarios = []
    if "generated_code" not in st.session_state:
        st.session_state.generated_code = ""
    if "test_results" not in st.session_state:
        st.session_state.test_results = None

    # Tab 1: Analysis
    with tab1:
        st.header("Component Analysis")
        col1, col2 = st.columns([3, 1])

        with col1:
            input_method = st.radio("Input Method", ["URL", "Raw HTML Code"], horizontal=True)

            if input_method == "URL":
                st.info(f"Analyzing URL: {target_url}")
                # In a real app, we would fetch the HTML here.
                # For this demo, we can mock it or use requests if simple enough,
                # but Playwright is better for JS-heavy sites.
                # Let's use requests for simplicity if possible, or just a mock/placeholder for "Raw HTML Code" input.
                if st.button("Fetch & Analyze URL"):
                    with st.spinner("Fetching URL content..."):
                        try:
                            from playwright.sync_api import sync_playwright
                            with sync_playwright() as p:
                                browser = p.chromium.launch(headless=True)
                                page = browser.new_page()
                                page.goto(target_url, wait_until="networkidle")
                                html_content = page.content()
                                browser.close()

                            parser = UIParser()
                            st.session_state.parsed_elements = parser.parse_html(html_content)
                            st.session_state.ui_structure = parser.extract_structure(html_content)
                            st.success(f"Successfully parsed {len(st.session_state.parsed_elements)} elements.")

                        except Exception as e:
                            st.error(f"Error fetching URL: {e}")

            else:
                raw_html = st.text_area("Paste HTML Code", height=300)
                if st.button("Analyze HTML"):
                    if raw_html:
                        parser = UIParser()
                        st.session_state.parsed_elements = parser.parse_html(raw_html)
                        st.session_state.ui_structure = parser.extract_structure(raw_html)
                        st.success(f"Successfully parsed {len(st.session_state.parsed_elements)} elements.")
                    else:
                        st.warning("Please paste some HTML code.")

        with col2:
            st.markdown("### Stats")
            if st.session_state.parsed_elements:
                df = pd.DataFrame([el.to_dict() for el in st.session_state.parsed_elements])
                st.dataframe(df)
                st.metric("Total Elements", len(df))
                st.metric("Buttons", len(df[df['tag'] == 'button']))
                st.metric("Inputs", len(df[df['tag'] == 'input']))

    # Tab 2: Generation
    with tab2:
        st.header("Test Generation")

        if not st.session_state.parsed_elements:
            st.warning("Please analyze UI components first.")
        else:
            if st.button("Generate Scenarios"):
                generator = TestGenerator(api_key=api_key, model_name=model_name)
                with st.spinner("Generating test scenarios..."):
                    scenarios = generator.generate_scenarios(st.session_state.parsed_elements)
                    st.session_state.scenarios = scenarios
                    st.success(f"Generated {len(scenarios)} scenarios.")

            if st.session_state.scenarios:
                st.markdown("### Scenarios")
                for i, scenario in enumerate(st.session_state.scenarios):
                    st.markdown(f"**{i+1}.** {scenario}")

                if st.button("Generate Playwright Code"):
                    generator = TestGenerator(api_key=api_key, model_name=model_name)
                    with st.spinner("Writing test code..."):
                        code = generator.generate_playwright_code(
                            st.session_state.scenarios,
                            target_url,
                            st.session_state.ui_structure
                        )
                        st.session_state.generated_code = code
                        st.success("Test code generated!")

            if st.session_state.generated_code:
                st.markdown("### Generated Code")
                st.code(st.session_state.generated_code, language="python")

                # Save to file
                if st.button("Save Test File"):
                    filename = f"test_generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
                    filepath = os.path.join(Config.GENERATED_TESTS_DIR, filename)
                    with open(filepath, "w") as f:
                        f.write(st.session_state.generated_code)
                    st.success(f"Saved to {filepath}")
                    st.session_state.current_test_file = filepath

    # Tab 3: Execution
    with tab3:
        st.header("Test Execution")

        test_file = st.session_state.get("current_test_file")
        if not test_file:
            st.warning("Please generate and save a test file first.")
            # Option to list existing files
            files = [f for f in os.listdir(Config.GENERATED_TESTS_DIR) if f.startswith("test_")]
            if files:
                selected_file = st.selectbox("Or select an existing file:", files)
                if selected_file:
                    test_file = os.path.join(Config.GENERATED_TESTS_DIR, selected_file)
                    st.session_state.current_test_file = test_file

        if test_file:
            st.info(f"Target Test File: `{test_file}`")
            if st.button("Run Tests"):
                runner = TestRunner(headless=headless_mode)
                with st.spinner("Running tests..."):
                    result = runner.run_tests(test_file)
                    st.session_state.test_results = result

                if result["success"]:
                    st.success("Tests passed successfully!")
                else:
                    st.error("Tests failed.")

                # Display Results
                col1, col2, col3 = st.columns(3)
                col1.metric("Passed", result.get("passed", 0))
                col2.metric("Failed", result.get("failed", 0))
                col3.metric("Total", result.get("total", 0))

                with st.expander("Show Output Logs"):
                    st.code(result.get("output", ""), language="text")

                # Self Healing
                if not result["success"] and result.get("failed", 0) > 0:
                    st.divider()
                    st.subheader("🩹 Self-Healing")
                    st.markdown("The agent can attempt to fix the failing tests based on the error logs.")

                    if st.button("Attempt Self-Heal"):
                        generator = TestGenerator(api_key=api_key, model_name=model_name)
                        with st.spinner("Analyzing error and fixing code..."):
                            # Read the current file content
                            with open(test_file, "r") as f:
                                current_code = f.read()

                            fixed_code = generator.self_heal(result.get("output", ""), current_code)

                            # Overwrite the file or save as new? Let's overwrite for "healing" or create a _fixed version.
                            # Let's create a fixed version.
                            fixed_filename = test_file.replace(".py", "_fixed.py")
                            with open(fixed_filename, "w") as f:
                                f.write(fixed_code)

                            st.success(f"Fixed code saved to `{fixed_filename}`")
                            st.session_state.current_test_file = fixed_filename
                            st.code(fixed_code, language="python")
                            st.info("You can now run the fixed test file.")

if __name__ == "__main__":
    main()
