# SQL to NoSQL Migrator

A premium AI agent application that converts SQL database schemas to MongoDB or DynamoDB equivalents, complete with migration scripts and documentation.

## Features

- **Schema Analysis**: Parses SQL `CREATE TABLE` statements.
- **Intelligent Conversion**: Suggests optimal NoSQL schema designs (Embedding vs Referencing) using LLM.
- **Multi-Target Support**: Generates schemas for MongoDB (BSON/JSON Schema) and DynamoDB (Table Definition).
- **Migration Scripts**: Auto-generates Python scripts to migrate data.
- **Documentation**: Produces comprehensive migration documentation.
- **Premium UI**: User-friendly Streamlit interface.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file in the project root:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    # Optional: Set to true to use mock LLM responses for testing
    USE_MOCK_LLM=true
    ```

3.  **Run Application**:
    ```bash
    streamlit run ui/app.py
    ```

## Testing

Run tests with `pytest`:

```bash
pytest
```
