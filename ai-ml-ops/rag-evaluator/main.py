import streamlit as st
import os
import sys
import tempfile
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config import Config
from agent.ingestion import load_document, split_documents
from agent.rag_pipeline import RAGPipeline
from agent.evaluator import RAGEvaluator

st.set_page_config(
    page_title="RAG Evaluator Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 RAG Evaluator Agent")
st.markdown("""
This agent evaluates the quality of your RAG pipeline by measuring:
- **Faithfulness**: Is the answer derived from the context?
- **Answer Relevance**: Is the answer relevant to the question?
- **Context Precision**: Is the retrieved context useful?
""")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    openai_api_key = st.text_input("OpenAI API Key", type="password", value=Config.OPENAI_API_KEY or "")
    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")
        st.stop()

    os.environ["OPENAI_API_KEY"] = openai_api_key

    model_name = st.selectbox(
        "LLM Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0
    )

    chunk_size = st.slider("Chunk Size", 100, 2000, Config.DEFAULT_CHUNK_SIZE, 100)
    chunk_overlap = st.slider("Chunk Overlap", 0, 500, Config.DEFAULT_CHUNK_OVERLAP, 50)

    top_k = st.slider("Top K Retrieval", 1, 10, Config.DEFAULT_K, 1)

    st.markdown("---")
    st.markdown("Built with LangChain & Streamlit")

# Session State Initialization
if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None
if "documents_ingested" not in st.session_state:
    st.session_state.documents_ingested = False
if "evaluation_results" not in st.session_state:
    st.session_state.evaluation_results = [] # List of DataFrames
if "current_results" not in st.session_state:
    st.session_state.current_results = None

# Tabs
tab1, tab2, tab3 = st.tabs(["📚 Knowledge Base", "🧪 Evaluation Dashboard", "📊 Comparison"])

# --- TAB 1: Knowledge Base ---
with tab1:
    st.header("📚 Knowledge Base Management")
    st.markdown("Upload documents (PDF or TXT) to create your RAG Knowledge Base.")

    uploaded_files = st.file_uploader("Upload Documents", type=["pdf", "txt"], accept_multiple_files=True)

    if st.button("Process and Index Documents"):
        if not uploaded_files:
            st.warning("Please upload at least one file.")
        else:
            with st.spinner("Processing documents..."):
                all_documents = []
                temp_dir = tempfile.mkdtemp()

                try:
                    for uploaded_file in uploaded_files:
                        # Save uploaded file to temp path
                        file_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        # Load documents
                        docs = load_document(file_path)
                        all_documents.extend(docs)

                    # Split documents
                    if all_documents:
                        st.info(f"Splitting {len(all_documents)} documents...")
                        split_docs = split_documents(all_documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                        st.write(f"Created {len(split_docs)} chunks.")

                        # Initialize Pipeline
                        st.info("Indexing into Vector Store...")
                        pipeline = RAGPipeline(openai_api_key=openai_api_key, model_name=model_name, k=top_k)
                        pipeline.index_documents(split_docs)

                        st.session_state.rag_pipeline = pipeline
                        st.session_state.documents_ingested = True
                        st.success("✅ Knowledge Base successfully indexed!")
                    else:
                        st.error("No documents loaded.")
                except Exception as e:
                    st.error(f"Error indexing documents: {e}")

# --- TAB 2: Evaluation Dashboard ---
with tab2:
    st.header("🧪 Evaluation Dashboard")

    if not st.session_state.documents_ingested:
        st.warning("⚠️ Please index documents in the 'Knowledge Base' tab first.")
    else:
        st.markdown("### 1. Upload Test Dataset")
        st.markdown("Upload a CSV or JSON file with a column named `question` (and optionally `ground_truth`).")

        test_file = st.file_uploader("Upload Test Dataset", type=["csv", "json"])
        test_data = None

        if test_file:
            try:
                if test_file.name.endswith(".csv"):
                    test_data = pd.read_csv(test_file)
                else:
                    test_data = pd.read_json(test_file)

                if "question" not in test_data.columns:
                    st.error("Dataset must contain a 'question' column.")
                    test_data = None
                else:
                    st.dataframe(test_data.head())
            except Exception as e:
                st.error(f"Error reading file: {e}")

        st.markdown("### 2. Run Evaluation")
        if st.button("🚀 Run Evaluation"):
            if test_data is None:
                st.warning("Please upload a valid test dataset.")
            else:
                evaluator = RAGEvaluator(openai_api_key=openai_api_key, model_name=model_name)
                results = []

                progress_bar = st.progress(0)
                status_text = st.empty()

                total_questions = len(test_data)

                for i, row in test_data.iterrows():
                    question = row["question"]
                    status_text.text(f"Processing ({i+1}/{total_questions}): {question}")

                    try:
                        # Retrieve and Generate
                        pipeline = st.session_state.rag_pipeline
                        retrieved_docs = pipeline.retrieve_context(question)
                        context_text = "\n\n".join([d.page_content for d in retrieved_docs])
                        answer = pipeline.query(question)

                        # Evaluate
                        scores = evaluator.evaluate(question, answer, context_text)

                        result_row = {
                            "question": question,
                            "answer": answer,
                            "context": context_text[:500] + "...", # Truncate for display
                            "faithfulness": scores["faithfulness"],
                            "answer_relevance": scores["answer_relevance"],
                            "context_precision": scores["context_precision"],
                            "latency": 0.0 # Placeholder
                        }
                        results.append(result_row)

                    except Exception as e:
                        st.error(f"Error processing question '{question}': {e}")

                    progress_bar.progress((i + 1) / total_questions)

                status_text.text("Evaluation Complete!")
                st.session_state.current_results = pd.DataFrame(results)

                # Save run to history
                run_name = f"Run {len(st.session_state.evaluation_results) + 1} ({time.strftime('%H:%M:%S')})"
                st.session_state.evaluation_results.append({
                    "name": run_name,
                    "config": {
                        "model": model_name,
                        "chunk_size": chunk_size,
                        "k": top_k
                    },
                    "data": st.session_state.current_results
                })

        if st.session_state.current_results is not None:
            df = st.session_state.current_results

            st.markdown("### 3. Results")

            # Metrics Summary
            col1, col2, col3 = st.columns(3)
            col1.metric("Avg Faithfulness", f"{df['faithfulness'].mean():.2f}")
            col2.metric("Avg Relevance", f"{df['answer_relevance'].mean():.2f}")
            col3.metric("Avg Context Precision", f"{df['context_precision'].mean():.2f}")

            # Radar Chart
            categories = ['Faithfulness', 'Answer Relevance', 'Context Precision']
            values = [df['faithfulness'].mean(), df['answer_relevance'].mean(), df['context_precision'].mean()]

            fig = px.line_polar(r=values, theta=categories, line_close=True)
            fig.update_traces(fill='toself')
            st.plotly_chart(fig)

            # Detailed Table
            st.markdown("#### Detailed Analysis")
            st.dataframe(df)

# --- TAB 3: Comparison ---
with tab3:
    st.header("📊 Run Comparison")

    if not st.session_state.evaluation_results:
        st.info("No runs available for comparison. Run an evaluation first.")
    else:
        run_options = [r["name"] for r in st.session_state.evaluation_results]
        selected_runs = st.multiselect("Select runs to compare", run_options, default=run_options)

        if selected_runs:
            comparison_data = []
            for run in st.session_state.evaluation_results:
                if run["name"] in selected_runs:
                    df = run["data"]
                    comparison_data.append({
                        "Run Name": run["name"],
                        "Model": run["config"]["model"],
                        "Chunk Size": run["config"]["chunk_size"],
                        "Top K": run["config"]["k"],
                        "Avg Faithfulness": df["faithfulness"].mean(),
                        "Avg Relevance": df["answer_relevance"].mean(),
                        "Avg Precision": df["context_precision"].mean()
                    })

            comp_df = pd.DataFrame(comparison_data)
            st.dataframe(comp_df)

            # Bar Chart Comparison
            fig_bar = px.bar(comp_df, x="Run Name", y=["Avg Faithfulness", "Avg Relevance", "Avg Precision"],
                             barmode="group", title="Metric Comparison across Runs")
            st.plotly_chart(fig_bar)
