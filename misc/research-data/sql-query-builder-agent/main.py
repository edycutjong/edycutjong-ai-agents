import streamlit as st
import pandas as pd
import plotly.express as px
from langchain_community.callbacks import StreamlitCallbackHandler

from agent.sql_agent import SQLQueryBuilder
from config import config

# Page Config
st.set_page_config(
    page_title="SQL Query Builder Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .stChatMessage {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box_shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #2c3e50;
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* Code block styling */
    code {
        color: #d63384;
    }

    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")

    api_key = st.text_input("OpenAI API Key", type="password", value=config.OPENAI_API_KEY or "")
    if not api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")

    db_uri = st.text_input("Database URI", value=config.DEFAULT_DB_URI)

    st.divider()
    st.markdown("### Schema Info")
    if api_key:
        try:
            agent = SQLQueryBuilder(db_uri=db_uri, api_key=api_key)
            schema_info = agent.get_schema()
            st.text_area("Database Schema", value=schema_info, height=300, disabled=True)
        except Exception as e:
            st.error(f"Could not connect to database: {e}")

# Main Chat Interface
st.title("🤖 SQL Query Builder Agent")
st.markdown("Ask questions about your data in natural language.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I can help you query your database. Ask me anything!"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sql" in msg:
            st.code(msg["sql"], language="sql")
        if "explanation" in msg:
            with st.expander("Explanation"):
                st.write(msg["explanation"])
        if "data" in msg:
            st.dataframe(msg["data"])
        if "chart" in msg:
            st.plotly_chart(msg["chart"], use_container_width=True)

if prompt := st.chat_input("Ex: Show me the top 5 users by order count"):
    if not api_key:
        st.error("Please provide an OpenAI API Key in the sidebar.")
        st.stop()

    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            with st.spinner("Analyzing request..."):
                agent = SQLQueryBuilder(db_uri=db_uri, api_key=api_key)

                # 1. Generate SQL
                sql_query = agent.generate_query(prompt)

                # 2. Validate SQL
                if not agent.validate_query(sql_query):
                    st.error("Generated query contains forbidden keywords (INSERT, UPDATE, DELETE, etc.). Operation aborted.")
                    st.stop()

                # 3. Explain SQL
                explanation = agent.explain_query(sql_query, prompt)

                # 4. Execute SQL
                df = agent.execute_query(sql_query)

                # Prepare response content
                response_content = "Here is what I found:"

                # Display components
                st.markdown(response_content)
                st.code(sql_query, language="sql")

                with st.expander("Explanation", expanded=True):
                    st.write(explanation)

                st.dataframe(df)

                # Visualization logic
                chart = None
                if not df.empty and len(df.columns) >= 2:
                    # Simple heuristic for visualization
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    categorical_cols = df.select_dtypes(include=['object', 'category']).columns

                    if len(numeric_cols) > 0 and len(categorical_cols) > 0:
                        x_col = categorical_cols[0]
                        y_col = numeric_cols[0]
                        st.markdown(f"**Visualizing {y_col} by {x_col}**")
                        chart = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                        st.plotly_chart(chart, use_container_width=True)
                    elif len(numeric_cols) >= 2:
                         st.markdown(f"**Visualizing {numeric_cols[0]} vs {numeric_cols[1]}**")
                         chart = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f"{numeric_cols[0]} vs {numeric_cols[1]}")
                         st.plotly_chart(chart, use_container_width=True)

                # Save to history
                msg_data = {
                    "role": "assistant",
                    "content": response_content,
                    "sql": sql_query,
                    "explanation": explanation,
                    "data": df
                }
                if chart:
                    msg_data["chart"] = chart

                st.session_state.messages.append(msg_data)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
