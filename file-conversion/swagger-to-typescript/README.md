# Swagger to TypeScript Agent

A premium AI-powered agent that converts OpenAPI/Swagger specifications into production-ready TypeScript API clients.

## Features

-   **AI-Driven Generation:** Uses LangChain and OpenAI to generate high-quality, context-aware TypeScript code.
-   **Flexible Parsing:** Supports both JSON and YAML formats, uploaded from file or fetched from URL.
-   **Configurable Output:**
    -   Choose between `axios` or `fetch` HTTP clients.
    -   Select Module System (ES Modules or CommonJS).
-   **Modern UI:** Built with Streamlit for a responsive and easy-to-use interface.

## Installation

1.  Navigate to the project directory:
    ```bash
    cd apps/agents/file-conversion/swagger-to-typescript
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Set your OpenAI API Key in `.env` or enter it in the UI.
2.  Run the application:
    ```bash
    streamlit run main.py
    ```
3.  Upload your Swagger file or enter a URL.
4.  Click "Generate TypeScript" and download your client.

## Testing

Run unit tests with pytest:
```bash
pytest tests/
```
