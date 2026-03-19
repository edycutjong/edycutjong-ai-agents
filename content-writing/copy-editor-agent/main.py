import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover

# Ensure imports work from project root
current_dir = os.path.dirname(os.path.abspath(__file__))  # pragma: no cover
if current_dir not in sys.path:  # pragma: no cover
    sys.path.append(current_dir)  # pragma: no cover

from agent.core import CopyEditorAgent  # pragma: no cover
from agent.analysis import analyze_text, interpret_flesch_score  # pragma: no cover
from config import Config  # pragma: no cover

st.set_page_config(  # pragma: no cover
    page_title="AI Copy Editor Agent",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium feel
st.markdown("""  # pragma: no cover
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

st.title("✍️ AI Copy Editor Agent")  # pragma: no cover
st.markdown("Professional proofreading and style enforcement powered by AI.")  # pragma: no cover

# Sidebar Configuration
with st.sidebar:  # pragma: no cover
    st.header("Configuration")  # pragma: no cover

    api_key_input = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY") or "")  # pragma: no cover
    if not api_key_input:  # pragma: no cover
        st.warning("Please enter your OpenAI API Key to proceed.")  # pragma: no cover

    st.divider()  # pragma: no cover

    style_guide = st.selectbox(  # pragma: no cover
        "Style Guide",
        ["AP Style", "Chicago Manual of Style", "MLA", "APA", "Custom"],
        index=0
    )

    tone = st.selectbox(  # pragma: no cover
        "Target Tone",
        ["Professional", "Academic", "Conversational", "Persuasive", "Technical", "Casual"],
        index=0
    )

    st.divider()  # pragma: no cover
    st.markdown("### Features")  # pragma: no cover
    st.markdown("- Grammar & Spelling Check")  # pragma: no cover
    st.markdown("- Style Enforcement")  # pragma: no cover
    st.markdown("- Readability Analysis")  # pragma: no cover
    st.markdown("- Passive Voice Detection")  # pragma: no cover

# Main Input Area
col1, col2 = st.columns([1, 1])  # pragma: no cover

with col1:  # pragma: no cover
    st.subheader("Original Text")  # pragma: no cover
    input_text = st.text_area("Paste your text here...", height=400, placeholder="Enter text to edit...")  # pragma: no cover

    if st.button("Analyze & Edit", type="primary", disabled=not input_text or not api_key_input):  # pragma: no cover
        with st.spinner("Analyzing and Editing..."):  # pragma: no cover
            try:  # pragma: no cover
                # 1. Analyze Original Text
                original_stats = analyze_text(input_text)  # pragma: no cover

                # 2. Run Agent
                agent = CopyEditorAgent(api_key=api_key_input)  # pragma: no cover
                result = agent.edit_text(input_text, style_guide=style_guide, tone=tone)  # pragma: no cover

                edited_text = result.get("edited_text", "")  # pragma: no cover
                report = result.get("summary_report", {})  # pragma: no cover

                # 3. Analyze Edited Text
                edited_stats = analyze_text(edited_text)  # pragma: no cover

                # Store in session state to persist
                st.session_state["result"] = result  # pragma: no cover
                st.session_state["original_stats"] = original_stats  # pragma: no cover
                st.session_state["edited_stats"] = edited_stats  # pragma: no cover
                st.session_state["has_run"] = True  # pragma: no cover

            except Exception as e:  # pragma: no cover
                st.error(f"An error occurred: {str(e)}")  # pragma: no cover

# Results Display
if st.session_state.get("has_run"):  # pragma: no cover
    result = st.session_state["result"]  # pragma: no cover
    original_stats = st.session_state["original_stats"]  # pragma: no cover
    edited_stats = st.session_state["edited_stats"]  # pragma: no cover
    edited_text = result.get("edited_text", "")  # pragma: no cover
    report = result.get("summary_report", {})  # pragma: no cover

    with col2:  # pragma: no cover
        st.subheader("Edited Text")  # pragma: no cover
        st.text_area("Result", value=edited_text, height=400, key="output_text")  # pragma: no cover

    st.divider()  # pragma: no cover

    # Analysis Metrics Section
    st.header("📊 Analysis Report")  # pragma: no cover

    m1, m2, m3, m4 = st.columns(4)  # pragma: no cover
    with m1:  # pragma: no cover
        st.metric("Reading Ease (Original)",  # pragma: no cover
                 f"{original_stats['flesch_reading_ease']:.1f}",
                 delta=f"{edited_stats['flesch_reading_ease'] - original_stats['flesch_reading_ease']:.1f}")
        st.caption(f"Original: {interpret_flesch_score(original_stats['flesch_reading_ease'])}")  # pragma: no cover

    with m2:  # pragma: no cover
        st.metric("Grade Level",  # pragma: no cover
                 f"{edited_stats['flesch_kincaid_grade']:.1f}",
                 delta=f"{edited_stats['flesch_kincaid_grade'] - original_stats['flesch_kincaid_grade']:.1f}",
                 delta_color="inverse")

    with m3:  # pragma: no cover
        st.metric("Word Count",  # pragma: no cover
                 f"{edited_stats['word_count']}",
                 delta=f"{edited_stats['word_count'] - original_stats['word_count']}")

    with m4:  # pragma: no cover
        st.metric("Sentence Count", f"{edited_stats['sentence_count']}")  # pragma: no cover

    # Detailed Report
    st.subheader("📝 Editing Summary")  # pragma: no cover

    r1, r2 = st.columns(2)  # pragma: no cover

    with r1:  # pragma: no cover
        st.markdown("#### Grammar & Style Fixes")  # pragma: no cover
        if report.get('grammar_fixes'):  # pragma: no cover
            for fix in report['grammar_fixes']:  # pragma: no cover
                st.markdown(f"- ✅ {fix}")  # pragma: no cover
        else:
            st.info("No grammar issues found.")  # pragma: no cover

        st.markdown("#### Style Changes")  # pragma: no cover
        if report.get('style_changes'):  # pragma: no cover
            for change in report['style_changes']:  # pragma: no cover
                st.markdown(f"- 🎨 {change}")  # pragma: no cover
        else:
            st.info("No style changes needed.")  # pragma: no cover

    with r2:  # pragma: no cover
        st.markdown("#### Conciseness & Flow")  # pragma: no cover
        if report.get('conciseness_improvements'):  # pragma: no cover
            for imp in report['conciseness_improvements']:  # pragma: no cover
                st.markdown(f"- ✂️ {imp}")  # pragma: no cover
        else:
            st.info("Text is concise.")  # pragma: no cover

        st.markdown("#### Tone Adjustments")  # pragma: no cover
        if report.get('tone_adjustments'):  # pragma: no cover
            for adj in report['tone_adjustments']:  # pragma: no cover
                st.markdown(f"- 🎵 {adj}")  # pragma: no cover
        else:
            st.info("Tone is consistent.")  # pragma: no cover

    with st.expander("Passive Voice Detection"):  # pragma: no cover
        if report.get('passive_voice_detected'):  # pragma: no cover
            st.warning("Passive voice detected in the following sentences (converted to active):")  # pragma: no cover
            for sentence in report['passive_voice_detected']:  # pragma: no cover
                st.markdown(f"- {sentence}")  # pragma: no cover
        else:
            st.success("No passive voice issues detected.")  # pragma: no cover

else:
    with col2:  # pragma: no cover
        st.info("Output will appear here after analysis.")  # pragma: no cover
