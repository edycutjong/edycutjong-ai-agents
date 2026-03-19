import streamlit as st  # pragma: no cover
import pandas as pd  # pragma: no cover
import plotly.express as px  # pragma: no cover
from langchain_community.callbacks import StreamlitCallbackHandler  # pragma: no cover

from agent.sql_agent import SQLQueryBuilder  # pragma: no cover
from config import config  # pragma: no cover

# Page Config
st.set_page_config(  # pragma: no cover
    page_title="SQL Query Builder Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown("""  # pragma: no cover
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
with st.sidebar:  # pragma: no cover
    st.title("⚙️ Configuration")  # pragma: no cover

    api_key = st.text_input("OpenAI API Key", type="password", value=config.OPENAI_API_KEY or "")  # pragma: no cover
    if not api_key:  # pragma: no cover
        st.warning("Please enter your OpenAI API Key to proceed.")  # pragma: no cover

    db_uri = st.text_input("Database URI", value=config.DEFAULT_DB_URI)  # pragma: no cover

    st.divider()  # pragma: no cover
    st.markdown("### Schema Info")  # pragma: no cover
    if api_key:  # pragma: no cover
        try:  # pragma: no cover
            agent = SQLQueryBuilder(db_uri=db_uri, api_key=api_key)  # pragma: no cover
            schema_info = agent.get_schema()  # pragma: no cover
            st.text_area("Database Schema", value=schema_info, height=300, disabled=True)  # pragma: no cover
        except Exception as e:  # pragma: no cover
            st.error(f"Could not connect to database: {e}")  # pragma: no cover

# Main Chat Interface
st.title("🤖 SQL Query Builder Agent")  # pragma: no cover
st.markdown("Ask questions about your data in natural language.")  # pragma: no cover

if "messages" not in st.session_state:  # pragma: no cover
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I can help you query your database. Ask me anything!"}]  # pragma: no cover

for msg in st.session_state.messages:  # pragma: no cover
    with st.chat_message(msg["role"]):  # pragma: no cover
        st.markdown(msg["content"])  # pragma: no cover
        if "sql" in msg:  # pragma: no cover
            st.code(msg["sql"], language="sql")  # pragma: no cover
        if "explanation" in msg:  # pragma: no cover
            with st.expander("Explanation"):  # pragma: no cover
                st.write(msg["explanation"])  # pragma: no cover
        if "data" in msg:  # pragma: no cover
            st.dataframe(msg["data"])  # pragma: no cover
        if "chart" in msg:  # pragma: no cover
            st.plotly_chart(msg["chart"], use_container_width=True)  # pragma: no cover

if prompt := st.chat_input("Ex: Show me the top 5 users by order count"):  # pragma: no cover
    if not api_key:  # pragma: no cover
        st.error("Please provide an OpenAI API Key in the sidebar.")  # pragma: no cover
        st.stop()  # pragma: no cover

    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})  # pragma: no cover
    with st.chat_message("user"):  # pragma: no cover
        st.markdown(prompt)  # pragma: no cover

    # Assistant response
    with st.chat_message("assistant"):  # pragma: no cover
        message_placeholder = st.empty()  # pragma: no cover
        full_response = ""  # pragma: no cover

        try:  # pragma: no cover
            with st.spinner("Analyzing request..."):  # pragma: no cover
                agent = SQLQueryBuilder(db_uri=db_uri, api_key=api_key)  # pragma: no cover

                # 1. Generate SQL
                sql_query = agent.generate_query(prompt)  # pragma: no cover

                # 2. Validate SQL
                if not agent.validate_query(sql_query):  # pragma: no cover
                    st.error("Generated query contains forbidden keywords (INSERT, UPDATE, DELETE, etc.). Operation aborted.")  # pragma: no cover
                    st.stop()  # pragma: no cover

                # 3. Explain SQL
                explanation = agent.explain_query(sql_query, prompt)  # pragma: no cover

                # 4. Execute SQL
                df = agent.execute_query(sql_query)  # pragma: no cover

                # Prepare response content
                response_content = "Here is what I found:"  # pragma: no cover

                # Display components
                st.markdown(response_content)  # pragma: no cover
                st.code(sql_query, language="sql")  # pragma: no cover

                with st.expander("Explanation", expanded=True):  # pragma: no cover
                    st.write(explanation)  # pragma: no cover

                st.dataframe(df)  # pragma: no cover

                # Visualization logic
                chart = None  # pragma: no cover
                if not df.empty and len(df.columns) >= 2:  # pragma: no cover
                    # Simple heuristic for visualization
                    numeric_cols = df.select_dtypes(include=['number']).columns  # pragma: no cover
                    categorical_cols = df.select_dtypes(include=['object', 'category']).columns  # pragma: no cover

                    if len(numeric_cols) > 0 and len(categorical_cols) > 0:  # pragma: no cover
                        x_col = categorical_cols[0]  # pragma: no cover
                        y_col = numeric_cols[0]  # pragma: no cover
                        st.markdown(f"**Visualizing {y_col} by {x_col}**")  # pragma: no cover
                        chart = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")  # pragma: no cover
                        st.plotly_chart(chart, use_container_width=True)  # pragma: no cover
                    elif len(numeric_cols) >= 2:  # pragma: no cover
                         st.markdown(f"**Visualizing {numeric_cols[0]} vs {numeric_cols[1]}**")  # pragma: no cover
                         chart = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f"{numeric_cols[0]} vs {numeric_cols[1]}")  # pragma: no cover
                         st.plotly_chart(chart, use_container_width=True)  # pragma: no cover

                # Save to history
                msg_data = {  # pragma: no cover
                    "role": "assistant",
                    "content": response_content,
                    "sql": sql_query,
                    "explanation": explanation,
                    "data": df
                }
                if chart:  # pragma: no cover
                    msg_data["chart"] = chart  # pragma: no cover

                st.session_state.messages.append(msg_data)  # pragma: no cover

        except Exception as e:  # pragma: no cover
            st.error(f"An error occurred: {str(e)}")  # pragma: no cover
