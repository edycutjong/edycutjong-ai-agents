import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import pandas as pd  # pragma: no cover
import numpy as np  # pragma: no cover
from agent.loader import DataLoader  # pragma: no cover
from agent.embedder import Embedder  # pragma: no cover
from agent.reducer import DimensionalityReducer  # pragma: no cover
from agent.analysis import Analyzer  # pragma: no cover
from agent.visualizer import Visualizer  # pragma: no cover
from agent.chat import ChatAgent  # pragma: no cover
from config import Config  # pragma: no cover
from langchain_text_splitters import RecursiveCharacterTextSplitter  # pragma: no cover

# Set page config
st.set_page_config(page_title="Embedding Explorer", layout="wide")  # pragma: no cover

# Title
st.title("🔍 Embedding Explorer")  # pragma: no cover

# Sidebar
with st.sidebar:  # pragma: no cover
    st.header("Configuration")  # pragma: no cover

    # API Key
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))  # pragma: no cover

    # Model Selection
    model_type = st.selectbox("Embedding Model", ["OpenAI", "HuggingFace"])  # pragma: no cover
    model_name = st.text_input("Model Name (Optional)", "")  # pragma: no cover

    # File Upload
    uploaded_file = st.file_uploader("Upload Data", type=['txt', 'pdf', 'csv'])  # pragma: no cover

    # Process Button
    if st.button("Process Data"):  # pragma: no cover
        if uploaded_file and (api_key or model_type == "HuggingFace"):  # pragma: no cover
            with st.spinner("Processing..."):  # pragma: no cover
                try:  # pragma: no cover
                    # Save uploaded file temporarily
                    temp_path = os.path.join(Config.DATA_DIR, uploaded_file.name)  # pragma: no cover
                    with open(temp_path, "wb") as f:  # pragma: no cover
                        f.write(uploaded_file.getbuffer())  # pragma: no cover

                    # Load Data
                    raw_content = DataLoader.load_file(temp_path)  # pragma: no cover

                    # Split Text
                    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)  # pragma: no cover
                    if isinstance(raw_content, str):  # pragma: no cover
                        texts = splitter.split_text(raw_content)  # pragma: no cover
                    elif isinstance(raw_content, list):  # pragma: no cover
                        texts = []  # pragma: no cover
                        for item in raw_content:  # pragma: no cover
                            texts.extend(splitter.split_text(str(item)))  # pragma: no cover
                    else:
                        texts = []  # pragma: no cover

                    if not texts:  # pragma: no cover
                        st.warning("No text extracted from file.")  # pragma: no cover
                        st.stop()  # pragma: no cover

                    st.session_state['texts'] = texts  # pragma: no cover

                    # Generate Embeddings
                    embedder = Embedder(model_type=model_type, model_name=model_name if model_name else None, api_key=api_key)  # pragma: no cover
                    embeddings = embedder.embed_documents(texts)  # pragma: no cover
                    st.session_state['embeddings'] = embeddings  # pragma: no cover
                    st.session_state['embedder'] = embedder # Store embedder for chat  # pragma: no cover

                    # Cleanup
                    if os.path.exists(temp_path):  # pragma: no cover
                        os.remove(temp_path)  # pragma: no cover

                    st.success(f"Processed {len(texts)} chunks.")  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.error(f"Error: {e}")  # pragma: no cover
        else:
            st.warning("Please upload a file and provide an API key (if using OpenAI).")  # pragma: no cover

# Main Content
if 'embeddings' in st.session_state:  # pragma: no cover
    embeddings = st.session_state['embeddings']  # pragma: no cover
    texts = st.session_state.get('texts', [])  # pragma: no cover

    tab1, tab2, tab3 = st.tabs(["Visualization", "Analysis", "Chat"])  # pragma: no cover

    with tab1:  # pragma: no cover
        st.subheader("Interactive Visualization")  # pragma: no cover
        col1, col2 = st.columns([1, 3])  # pragma: no cover

        with col1:  # pragma: no cover
            dim_method = st.selectbox("Reduction Method", ["PCA", "t-SNE", "UMAP"])  # pragma: no cover
            n_components = st.radio("Dimensions", [2, 3])  # pragma: no cover
            perplexity = st.slider("Perplexity (t-SNE)", 5, 50, 30)  # pragma: no cover

            if st.button("Update Plot"):  # pragma: no cover
                reducer = DimensionalityReducer(method=dim_method, n_components=n_components, perplexity=perplexity)  # pragma: no cover
                reduced_embeddings = reducer.reduce(embeddings)  # pragma: no cover
                st.session_state['reduced_embeddings'] = reduced_embeddings  # pragma: no cover

        with col2:  # pragma: no cover
            if 'reduced_embeddings' not in st.session_state:  # pragma: no cover
                # Initial reduction
                reducer = DimensionalityReducer(method="pca", n_components=2)  # pragma: no cover
                st.session_state['reduced_embeddings'] = reducer.reduce(embeddings)  # pragma: no cover

            # Clustering for color
            clusters = Analyzer.find_clusters(embeddings, n_clusters=5)  # pragma: no cover

            fig = Visualizer.create_scatter_plot(  # pragma: no cover
                st.session_state['reduced_embeddings'],
                labels=clusters,
                hover_data=texts,
                title=f"Embeddings ({dim_method} - {n_components}D)"
            )
            st.plotly_chart(fig, use_container_width=True)  # pragma: no cover

    with tab2:  # pragma: no cover
        st.subheader("Data Analysis")  # pragma: no cover

        st.write(f"**Total Chunks:** {len(texts)}")  # pragma: no cover
        st.write(f"**Embedding Dimensions:** {embeddings.shape[1]}")  # pragma: no cover

        # Outliers
        if st.checkbox("Detect Outliers"):  # pragma: no cover
            outliers = Analyzer.find_outliers(embeddings)  # pragma: no cover
            n_outliers = np.sum(outliers == -1)  # pragma: no cover
            st.write(f"Found {n_outliers} outliers.")  # pragma: no cover

            outlier_indices = np.where(outliers == -1)[0]  # pragma: no cover
            if len(outlier_indices) > 0:  # pragma: no cover
                st.write("Outlier Examples:")  # pragma: no cover
                for idx in outlier_indices[:5]:  # pragma: no cover
                    st.text(texts[idx][:200] + "...")  # pragma: no cover

    with tab3:  # pragma: no cover
        st.subheader("Chat with Data")  # pragma: no cover
        user_query = st.text_input("Ask a question about your data:")  # pragma: no cover
        if user_query:  # pragma: no cover
            if api_key:  # pragma: no cover
                # Re-initialize embedder if stored one lost (shouldn't happen in session state but good to be safe)
                # But embedder might not be serializable/pickleable for session state?
                # Embedder contains API key and model object. LangChain objects are usually pickleable.
                # If not, we recreate it.
                current_embedder = st.session_state.get('embedder')  # pragma: no cover
                if not current_embedder:  # pragma: no cover
                     current_embedder = Embedder(model_type=model_type, model_name=model_name if model_name else None, api_key=api_key)  # pragma: no cover

                agent = ChatAgent(embeddings, texts, api_key, current_embedder)  # pragma: no cover
                response = agent.run(user_query)  # pragma: no cover
                st.write(response)  # pragma: no cover
            else:
                st.warning("Please provide an OpenAI API Key to use the chat feature.")  # pragma: no cover
else:
    st.info("👈 Please upload a file to get started.")  # pragma: no cover
