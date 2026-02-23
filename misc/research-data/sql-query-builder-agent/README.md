# SQL Query Builder Agent

This is a Streamlit application that uses LangChain and OpenAI to convert natural language queries into SQL. It features a premium UI with schema introspection, query execution, and visual result preview.

## Setup

1.  **Clone the repository.**
2.  **Navigate to the project directory:**
    ```bash
    cd apps/agents/sql-query-builder-agent/
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file:**
    ```
    OPENAI_API_KEY=your_openai_api_key
    ```
5.  **Run the application:**
    ```bash
    streamlit run main.py
    ```

## Features

-   **Schema Introspection:** Automatically detects tables and columns.
-   **Natural Language to SQL:** Convert questions to SQL queries.
-   **Interactive Visualization:** View results in tables and charts (Plotly).
-   **Premium UI:** Custom styling with modern fonts and gradients.
-   **Query Explanation:** Understand how the SQL was generated.

## Testing

Run tests with `pytest`:

```bash
pytest tests/
```
