import streamlit as st
import os
import tempfile
import json
from agent.pdf_parser import extract_text_from_pdf
from agent.summarizer import PaperSummarizer
from agent.visualizer import Visualizer
from agent.reading_list import ReadingListGenerator
from agent.batch_processor import BatchProcessor

st.set_page_config(page_title="Paper Summarizer Agent", layout="wide")

st.title("📚 Paper Summarizer Agent")
st.markdown("Your AI-powered research assistant for summarizing papers, generating reading lists, and batch processing.")

tab1, tab2, tab3 = st.tabs(["Single Paper", "Batch Processing", "Reading List"])

with tab1:
    st.header("Summarize a Single Paper")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Extracting text..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            text = extract_text_from_pdf(tmp_path)
            os.remove(tmp_path)

        if text:
            st.success("Text extracted successfully!")

            if st.button("Generate Summary"):
                summarizer = PaperSummarizer()
                with st.spinner("Generating summary..."):
                    summary = summarizer.summarize_all(text)

                st.subheader("Abstract & Methodology")
                st.markdown(summary["abstract_methodology"])

                st.subheader("Plain Language Summary")
                st.markdown(summary["plain_language_summary"])

                st.subheader("Key Findings")
                st.markdown(summary["key_findings"])

                st.subheader("Citations")
                st.markdown(summary["citations"])

                st.subheader("Visual Summary")
                visualizer = Visualizer()
                with st.spinner("Generating visual summary..."):
                    visual_summary = visualizer.generate_visual_summary(text)

                # Check if visual_summary contains mermaid block or is raw code
                if "```mermaid" not in visual_summary:
                    st.markdown(f"```mermaid\n{visual_summary}\n```")
                else:
                    st.markdown(visual_summary)

with tab2:
    st.header("Batch Processing")
    st.markdown("Enter the path to a directory containing PDF files.")
    directory = st.text_input("Directory Path")

    if st.button("Process Directory"):
        if directory and os.path.isdir(directory):
            processor = BatchProcessor()
            with st.spinner("Processing directory..."):
                results = processor.process_directory(directory)

            st.success(f"Processed {len(results)} files.")
            st.json(results)

            # Allow download
            json_str = json.dumps(results, indent=2)
            st.download_button(
                label="Download Results (JSON)",
                data=json_str,
                file_name="batch_summaries.json",
                mime="application/json"
            )
        else:
            st.error("Invalid directory path.")

with tab3:
    st.header("Generate Reading List")
    topic = st.text_input("Enter a research topic")

    if st.button("Generate List"):
        if topic:
            generator = ReadingListGenerator()
            with st.spinner("Generating reading list..."):
                reading_list = generator.generate_reading_list(topic)
            st.markdown(reading_list)
        else:
            st.error("Please enter a topic.")
