import streamlit as st
import os
import sys

# Ensure imports work from project root
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from agent.core import CopyEditorAgent
from agent.analysis import analyze_text, interpret_flesch_score
from config import Config

st.set_page_config(
    page_title="AI Copy Editor Agent",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium feel
st.markdown("""
<style>
    .stTextArea textarea {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
    }
    .metric-container {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .report-card {
        border: 1px solid #4F4F4F;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("✍️ AI Copy Editor Agent")
st.markdown("Professional proofreading and style enforcement powered by AI.")

# Sidebar Configuration
with st.sidebar:
    st.header("Configuration")

    api_key_input = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY") or "")
    if not api_key_input:
        st.warning("Please enter your OpenAI API Key to proceed.")

    st.divider()

    style_guide = st.selectbox(
        "Style Guide",
        ["AP Style", "Chicago Manual of Style", "MLA", "APA", "Custom"],
        index=0
    )

    tone = st.selectbox(
        "Target Tone",
        ["Professional", "Academic", "Conversational", "Persuasive", "Technical", "Casual"],
        index=0
    )

    st.divider()
    st.markdown("### Features")
    st.markdown("- Grammar & Spelling Check")
    st.markdown("- Style Enforcement")
    st.markdown("- Readability Analysis")
    st.markdown("- Passive Voice Detection")

# Main Input Area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Original Text")
    input_text = st.text_area("Paste your text here...", height=400, placeholder="Enter text to edit...")

    if st.button("Analyze & Edit", type="primary", disabled=not input_text or not api_key_input):
        with st.spinner("Analyzing and Editing..."):
            try:
                # 1. Analyze Original Text
                original_stats = analyze_text(input_text)

                # 2. Run Agent
                agent = CopyEditorAgent(api_key=api_key_input)
                result = agent.edit_text(input_text, style_guide=style_guide, tone=tone)

                edited_text = result.get("edited_text", "")
                report = result.get("summary_report", {})

                # 3. Analyze Edited Text
                edited_stats = analyze_text(edited_text)

                # Store in session state to persist
                st.session_state["result"] = result
                st.session_state["original_stats"] = original_stats
                st.session_state["edited_stats"] = edited_stats
                st.session_state["has_run"] = True

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Results Display
if st.session_state.get("has_run"):
    result = st.session_state["result"]
    original_stats = st.session_state["original_stats"]
    edited_stats = st.session_state["edited_stats"]
    edited_text = result.get("edited_text", "")
    report = result.get("summary_report", {})

    with col2:
        st.subheader("Edited Text")
        st.text_area("Result", value=edited_text, height=400, key="output_text")

    st.divider()

    # Analysis Metrics Section
    st.header("📊 Analysis Report")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Reading Ease (Original)",
                 f"{original_stats['flesch_reading_ease']:.1f}",
                 delta=f"{edited_stats['flesch_reading_ease'] - original_stats['flesch_reading_ease']:.1f}")
        st.caption(f"Original: {interpret_flesch_score(original_stats['flesch_reading_ease'])}")

    with m2:
        st.metric("Grade Level",
                 f"{edited_stats['flesch_kincaid_grade']:.1f}",
                 delta=f"{edited_stats['flesch_kincaid_grade'] - original_stats['flesch_kincaid_grade']:.1f}",
                 delta_color="inverse")

    with m3:
        st.metric("Word Count",
                 f"{edited_stats['word_count']}",
                 delta=f"{edited_stats['word_count'] - original_stats['word_count']}")

    with m4:
        st.metric("Sentence Count", f"{edited_stats['sentence_count']}")

    # Detailed Report
    st.subheader("📝 Editing Summary")

    r1, r2 = st.columns(2)

    with r1:
        st.markdown("#### Grammar & Style Fixes")
        if report.get('grammar_fixes'):
            for fix in report['grammar_fixes']:
                st.markdown(f"- ✅ {fix}")
        else:
            st.info("No grammar issues found.")

        st.markdown("#### Style Changes")
        if report.get('style_changes'):
            for change in report['style_changes']:
                st.markdown(f"- 🎨 {change}")
        else:
            st.info("No style changes needed.")

    with r2:
        st.markdown("#### Conciseness & Flow")
        if report.get('conciseness_improvements'):
            for imp in report['conciseness_improvements']:
                st.markdown(f"- ✂️ {imp}")
        else:
            st.info("Text is concise.")

        st.markdown("#### Tone Adjustments")
        if report.get('tone_adjustments'):
            for adj in report['tone_adjustments']:
                st.markdown(f"- 🎵 {adj}")
        else:
            st.info("Tone is consistent.")

    with st.expander("Passive Voice Detection"):
        if report.get('passive_voice_detected'):
            st.warning("Passive voice detected in the following sentences (converted to active):")
            for sentence in report['passive_voice_detected']:
                st.markdown(f"- {sentence}")
        else:
            st.success("No passive voice issues detected.")

else:
    with col2:
        st.info("Output will appear here after analysis.")
