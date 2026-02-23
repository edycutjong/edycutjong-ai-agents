import streamlit as st
import os
import pandas as pd
import numpy as np
from agent.loader import DataLoader
from agent.embedder import Embedder
from agent.reducer import DimensionalityReducer
from agent.analysis import Analyzer
from agent.visualizer import Visualizer
from agent.chat import ChatAgent
from config import Config
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Set page config
st.set_page_config(page_title="Embedding Explorer", layout="wide")

# Title
st.title("🔍 Embedding Explorer")

# Sidebar
with st.sidebar:
    st.header("Configuration")

    # API Key
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))

    # Model Selection
    model_type = st.selectbox("Embedding Model", ["OpenAI", "HuggingFace"])
    model_name = st.text_input("Model Name (Optional)", "")

    # File Upload
    uploaded_file = st.file_uploader("Upload Data", type=['txt', 'pdf', 'csv'])

    # Process Button
    if st.button("Process Data"):
        if uploaded_file and (api_key or model_type == "HuggingFace"):
            with st.spinner("Processing..."):
                try:
                    # Save uploaded file temporarily
                    temp_path = os.path.join(Config.DATA_DIR, uploaded_file.name)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Load Data
                    raw_content = DataLoader.load_file(temp_path)

                    # Split Text
                    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                    if isinstance(raw_content, str):
                        texts = splitter.split_text(raw_content)
                    elif isinstance(raw_content, list):
                        texts = []
                        for item in raw_content:
                            texts.extend(splitter.split_text(str(item)))
                    else:
                        texts = []

                    if not texts:
                        st.warning("No text extracted from file.")
                        st.stop()

                    st.session_state['texts'] = texts

                    # Generate Embeddings
                    embedder = Embedder(model_type=model_type, model_name=model_name if model_name else None, api_key=api_key)
                    embeddings = embedder.embed_documents(texts)
                    st.session_state['embeddings'] = embeddings
                    st.session_state['embedder'] = embedder # Store embedder for chat

                    # Cleanup
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

                    st.success(f"Processed {len(texts)} chunks.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please upload a file and provide an API key (if using OpenAI).")

# Main Content
if 'embeddings' in st.session_state:
    embeddings = st.session_state['embeddings']
    texts = st.session_state.get('texts', [])

    tab1, tab2, tab3 = st.tabs(["Visualization", "Analysis", "Chat"])

    with tab1:
        st.subheader("Interactive Visualization")
        col1, col2 = st.columns([1, 3])

        with col1:
            dim_method = st.selectbox("Reduction Method", ["PCA", "t-SNE", "UMAP"])
            n_components = st.radio("Dimensions", [2, 3])
            perplexity = st.slider("Perplexity (t-SNE)", 5, 50, 30)

            if st.button("Update Plot"):
                reducer = DimensionalityReducer(method=dim_method, n_components=n_components, perplexity=perplexity)
                reduced_embeddings = reducer.reduce(embeddings)
                st.session_state['reduced_embeddings'] = reduced_embeddings

        with col2:
            if 'reduced_embeddings' not in st.session_state:
                # Initial reduction
                reducer = DimensionalityReducer(method="pca", n_components=2)
                st.session_state['reduced_embeddings'] = reducer.reduce(embeddings)

            # Clustering for color
            clusters = Analyzer.find_clusters(embeddings, n_clusters=5)

            fig = Visualizer.create_scatter_plot(
                st.session_state['reduced_embeddings'],
                labels=clusters,
                hover_data=texts,
                title=f"Embeddings ({dim_method} - {n_components}D)"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Data Analysis")

        st.write(f"**Total Chunks:** {len(texts)}")
        st.write(f"**Embedding Dimensions:** {embeddings.shape[1]}")

        # Outliers
        if st.checkbox("Detect Outliers"):
            outliers = Analyzer.find_outliers(embeddings)
            n_outliers = np.sum(outliers == -1)
            st.write(f"Found {n_outliers} outliers.")

            outlier_indices = np.where(outliers == -1)[0]
            if len(outlier_indices) > 0:
                st.write("Outlier Examples:")
                for idx in outlier_indices[:5]:
                    st.text(texts[idx][:200] + "...")

    with tab3:
        st.subheader("Chat with Data")
        user_query = st.text_input("Ask a question about your data:")
        if user_query:
            if api_key:
                # Re-initialize embedder if stored one lost (shouldn't happen in session state but good to be safe)
                # But embedder might not be serializable/pickleable for session state?
                # Embedder contains API key and model object. LangChain objects are usually pickleable.
                # If not, we recreate it.
                current_embedder = st.session_state.get('embedder')
                if not current_embedder:
                     current_embedder = Embedder(model_type=model_type, model_name=model_name if model_name else None, api_key=api_key)

                agent = ChatAgent(embeddings, texts, api_key, current_embedder)
                response = agent.run(user_query)
                st.write(response)
            else:
                st.warning("Please provide an OpenAI API Key to use the chat feature.")
else:
    st.info("👈 Please upload a file to get started.")
