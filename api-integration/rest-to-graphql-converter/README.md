# REST to GraphQL Converter

This application is an AI-powered agent that converts REST API specifications (OpenAPI/Swagger) into a production-ready GraphQL schema, resolvers, and a migration guide.

## Features

*   **Parse OpenAPI/Swagger**: Supports JSON and YAML formats.
*   **Generate GraphQL Schema**: Creates Types, Queries, and Mutations based on your REST endpoints.
*   **Generate Resolvers**: outputs resolver code in Python (default), Node.js, or TypeScript.
*   **Migration Guide**: Generates a markdown guide to help you transition from REST to GraphQL.
*   **Premium UI**: Built with Streamlit for a smooth user experience.

## Installation

1.  Navigate to the project directory:
    ```bash
    cd apps/agents/api-integration/rest-to-graphql-converter/
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Set up environment variables:
    *   Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        ```
    *   Add your OpenAI API Key to `.env`.

## Usage

Run the Streamlit application:

```bash
streamlit run main.py
```

Or convert via CLI (Python script usage example):

```python
from agent.converter import RestToGraphqlConverter

converter = RestToGraphqlConverter(api_key="your-key")
result = converter.convert('{"openapi": "3.0.0", ...}')
print(result['schema'])
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Project Structure

*   `agent/`: Core agent logic (Parser, Generator, Converter).
*   `prompts/`: LangChain prompt templates.
*   `tests/`: Unit and integration tests.
*   `main.py`: Streamlit application entry point.
*   `config.py`: Configuration settings.
