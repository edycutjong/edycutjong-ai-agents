import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover
import tempfile  # pragma: no cover
import pandas as pd  # pragma: no cover
import plotly.express as px  # pragma: no cover
import plotly.graph_objects as go  # pragma: no cover
import time  # pragma: no cover

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # pragma: no cover

from config import Config  # pragma: no cover
from agent.ingestion import load_document, split_documents  # pragma: no cover
from agent.rag_pipeline import RAGPipeline  # pragma: no cover
from agent.evaluator import RAGEvaluator  # pragma: no cover

st.set_page_config(  # pragma: no cover
    page_title="RAG Evaluator Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 RAG Evaluator Agent")  # pragma: no cover
st.markdown("""  # pragma: no cover
This agent evaluates the quality of your RAG pipeline by measuring:
- **Faithfulness**: Is the answer derived from the context?
- **Answer Relevance**: Is the answer relevant to the question?
- **Context Precision**: Is the retrieved context useful?
""")

# Sidebar Configuration
with st.sidebar:  # pragma: no cover
    st.header("⚙️ Configuration")  # pragma: no cover

    openai_api_key = st.text_input("OpenAI API Key", type="password", value=Config.OPENAI_API_KEY or "")  # pragma: no cover
    if not openai_api_key:  # pragma: no cover
        st.warning("Please enter your OpenAI API Key to proceed.")  # pragma: no cover
        st.stop()  # pragma: no cover

    os.environ["OPENAI_API_KEY"] = openai_api_key  # pragma: no cover

    model_name = st.selectbox(  # pragma: no cover
        "LLM Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0
    )

    chunk_size = st.slider("Chunk Size", 100, 2000, Config.DEFAULT_CHUNK_SIZE, 100)  # pragma: no cover
    chunk_overlap = st.slider("Chunk Overlap", 0, 500, Config.DEFAULT_CHUNK_OVERLAP, 50)  # pragma: no cover

    top_k = st.slider("Top K Retrieval", 1, 10, Config.DEFAULT_K, 1)  # pragma: no cover

    st.markdown("---")  # pragma: no cover
    st.markdown("Built with LangChain & Streamlit")  # pragma: no cover

# Session State Initialization
if "rag_pipeline" not in st.session_state:  # pragma: no cover
    st.session_state.rag_pipeline = None  # pragma: no cover
if "documents_ingested" not in st.session_state:  # pragma: no cover
    st.session_state.documents_ingested = False  # pragma: no cover
if "evaluation_results" not in st.session_state:  # pragma: no cover
    st.session_state.evaluation_results = [] # List of DataFrames  # pragma: no cover
if "current_results" not in st.session_state:  # pragma: no cover
    st.session_state.current_results = None  # pragma: no cover

# Tabs
tab1, tab2, tab3 = st.tabs(["📚 Knowledge Base", "🧪 Evaluation Dashboard", "📊 Comparison"])  # pragma: no cover

# --- TAB 1: Knowledge Base ---
with tab1:  # pragma: no cover
    st.header("📚 Knowledge Base Management")  # pragma: no cover
    st.markdown("Upload documents (PDF or TXT) to create your RAG Knowledge Base.")  # pragma: no cover

    uploaded_files = st.file_uploader("Upload Documents", type=["pdf", "txt"], accept_multiple_files=True)  # pragma: no cover

    if st.button("Process and Index Documents"):  # pragma: no cover
        if not uploaded_files:  # pragma: no cover
            st.warning("Please upload at least one file.")  # pragma: no cover
        else:
            with st.spinner("Processing documents..."):  # pragma: no cover
                all_documents = []  # pragma: no cover
                temp_dir = tempfile.mkdtemp()  # pragma: no cover

                try:  # pragma: no cover
                    for uploaded_file in uploaded_files:  # pragma: no cover
                        # Save uploaded file to temp path
                        file_path = os.path.join(temp_dir, uploaded_file.name)  # pragma: no cover
                        with open(file_path, "wb") as f:  # pragma: no cover
                            f.write(uploaded_file.getbuffer())  # pragma: no cover

                        # Load documents
                        docs = load_document(file_path)  # pragma: no cover
                        all_documents.extend(docs)  # pragma: no cover

                    # Split documents
                    if all_documents:  # pragma: no cover
                        st.info(f"Splitting {len(all_documents)} documents...")  # pragma: no cover
                        split_docs = split_documents(all_documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)  # pragma: no cover
                        st.write(f"Created {len(split_docs)} chunks.")  # pragma: no cover

                        # Initialize Pipeline
                        st.info("Indexing into Vector Store...")  # pragma: no cover
                        pipeline = RAGPipeline(openai_api_key=openai_api_key, model_name=model_name, k=top_k)  # pragma: no cover
                        pipeline.index_documents(split_docs)  # pragma: no cover

                        st.session_state.rag_pipeline = pipeline  # pragma: no cover
                        st.session_state.documents_ingested = True  # pragma: no cover
                        st.success("✅ Knowledge Base successfully indexed!")  # pragma: no cover
                    else:
                        st.error("No documents loaded.")  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.error(f"Error indexing documents: {e}")  # pragma: no cover

# --- TAB 2: Evaluation Dashboard ---
with tab2:  # pragma: no cover
    st.header("🧪 Evaluation Dashboard")  # pragma: no cover

    if not st.session_state.documents_ingested:  # pragma: no cover
        st.warning("⚠️ Please index documents in the 'Knowledge Base' tab first.")  # pragma: no cover
    else:
        st.markdown("### 1. Upload Test Dataset")  # pragma: no cover
        st.markdown("Upload a CSV or JSON file with a column named `question` (and optionally `ground_truth`).")  # pragma: no cover

        test_file = st.file_uploader("Upload Test Dataset", type=["csv", "json"])  # pragma: no cover
        test_data = None  # pragma: no cover

        if test_file:  # pragma: no cover
            try:  # pragma: no cover
                if test_file.name.endswith(".csv"):  # pragma: no cover
                    test_data = pd.read_csv(test_file)  # pragma: no cover
                else:
                    test_data = pd.read_json(test_file)  # pragma: no cover

                if "question" not in test_data.columns:  # pragma: no cover
                    st.error("Dataset must contain a 'question' column.")  # pragma: no cover
                    test_data = None  # pragma: no cover
                else:
                    st.dataframe(test_data.head())  # pragma: no cover
            except Exception as e:  # pragma: no cover
                st.error(f"Error reading file: {e}")  # pragma: no cover

        st.markdown("### 2. Run Evaluation")  # pragma: no cover
        if st.button("🚀 Run Evaluation"):  # pragma: no cover
            if test_data is None:  # pragma: no cover
                st.warning("Please upload a valid test dataset.")  # pragma: no cover
            else:
                evaluator = RAGEvaluator(openai_api_key=openai_api_key, model_name=model_name)  # pragma: no cover
                results = []  # pragma: no cover

                progress_bar = st.progress(0)  # pragma: no cover
                status_text = st.empty()  # pragma: no cover

                total_questions = len(test_data)  # pragma: no cover

                for i, row in test_data.iterrows():  # pragma: no cover
                    question = row["question"]  # pragma: no cover
                    status_text.text(f"Processing ({i+1}/{total_questions}): {question}")  # pragma: no cover

                    try:  # pragma: no cover
                        # Retrieve and Generate
                        pipeline = st.session_state.rag_pipeline  # pragma: no cover
                        retrieved_docs = pipeline.retrieve_context(question)  # pragma: no cover
                        context_text = "\n\n".join([d.page_content for d in retrieved_docs])  # pragma: no cover
                        answer = pipeline.query(question)  # pragma: no cover

                        # Evaluate
                        scores = evaluator.evaluate(question, answer, context_text)  # pragma: no cover

                        result_row = {  # pragma: no cover
                            "question": question,
                            "answer": answer,
                            "context": context_text[:500] + "...", # Truncate for display
                            "faithfulness": scores["faithfulness"],
                            "answer_relevance": scores["answer_relevance"],
                            "context_precision": scores["context_precision"],
                            "latency": 0.0 # Placeholder
                        }
                        results.append(result_row)  # pragma: no cover

                    except Exception as e:  # pragma: no cover
                        st.error(f"Error processing question '{question}': {e}")  # pragma: no cover

                    progress_bar.progress((i + 1) / total_questions)  # pragma: no cover

                status_text.text("Evaluation Complete!")  # pragma: no cover
                st.session_state.current_results = pd.DataFrame(results)  # pragma: no cover

                # Save run to history
                run_name = f"Run {len(st.session_state.evaluation_results) + 1} ({time.strftime('%H:%M:%S')})"  # pragma: no cover
                st.session_state.evaluation_results.append({  # pragma: no cover
                    "name": run_name,
                    "config": {
                        "model": model_name,
                        "chunk_size": chunk_size,
                        "k": top_k
                    },
                    "data": st.session_state.current_results
                })

        if st.session_state.current_results is not None:  # pragma: no cover
            df = st.session_state.current_results  # pragma: no cover

            st.markdown("### 3. Results")  # pragma: no cover

            # Metrics Summary
            col1, col2, col3 = st.columns(3)  # pragma: no cover
            col1.metric("Avg Faithfulness", f"{df['faithfulness'].mean():.2f}")  # pragma: no cover
            col2.metric("Avg Relevance", f"{df['answer_relevance'].mean():.2f}")  # pragma: no cover
            col3.metric("Avg Context Precision", f"{df['context_precision'].mean():.2f}")  # pragma: no cover

            # Radar Chart
            categories = ['Faithfulness', 'Answer Relevance', 'Context Precision']  # pragma: no cover
            values = [df['faithfulness'].mean(), df['answer_relevance'].mean(), df['context_precision'].mean()]  # pragma: no cover

            fig = px.line_polar(r=values, theta=categories, line_close=True)  # pragma: no cover
            fig.update_traces(fill='toself')  # pragma: no cover
            st.plotly_chart(fig)  # pragma: no cover

            # Detailed Table
            st.markdown("#### Detailed Analysis")  # pragma: no cover
            st.dataframe(df)  # pragma: no cover

# --- TAB 3: Comparison ---
with tab3:  # pragma: no cover
    st.header("📊 Run Comparison")  # pragma: no cover

    if not st.session_state.evaluation_results:  # pragma: no cover
        st.info("No runs available for comparison. Run an evaluation first.")  # pragma: no cover
    else:
        run_options = [r["name"] for r in st.session_state.evaluation_results]  # pragma: no cover
        selected_runs = st.multiselect("Select runs to compare", run_options, default=run_options)  # pragma: no cover

        if selected_runs:  # pragma: no cover
            comparison_data = []  # pragma: no cover
            for run in st.session_state.evaluation_results:  # pragma: no cover
                if run["name"] in selected_runs:  # pragma: no cover
                    df = run["data"]  # pragma: no cover
                    comparison_data.append({  # pragma: no cover
                        "Run Name": run["name"],
                        "Model": run["config"]["model"],
                        "Chunk Size": run["config"]["chunk_size"],
                        "Top K": run["config"]["k"],
                        "Avg Faithfulness": df["faithfulness"].mean(),
                        "Avg Relevance": df["answer_relevance"].mean(),
                        "Avg Precision": df["context_precision"].mean()
                    })

            comp_df = pd.DataFrame(comparison_data)  # pragma: no cover
            st.dataframe(comp_df)  # pragma: no cover

            # Bar Chart Comparison
            fig_bar = px.bar(comp_df, x="Run Name", y=["Avg Faithfulness", "Avg Relevance", "Avg Precision"],  # pragma: no cover
                             barmode="group", title="Metric Comparison across Runs")
            st.plotly_chart(fig_bar)  # pragma: no cover
