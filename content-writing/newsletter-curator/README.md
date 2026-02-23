# Newsletter Curator Agent

An AI-powered agent that aggregates, filters, summarizes, and formats tech news from RSS feeds into a premium newsletter.

## Features

- **Multi-Source Aggregation**: Fetches articles from configurable RSS feeds (TechCrunch, Hacker News, The Verge, etc.).
- **Smart Filtering**: Uses LLMs (OpenAI or Google Gemini) to filter articles based on your specific topics of interest.
- **Concise Summaries**: Generates high-quality, bullet-point summaries for each relevant article.
- **Categorization & Ranking**: Automatically categorizes stories and scores them by importance (1-10).
- **Premium Formatting**: Outputs a polished newsletter in Markdown and HTML formats.
- **Interactive UI**: Built with Streamlit for a seamless user experience.

## Setup

1.  **Navigate to the project directory:**
    ```bash
    cd apps/agents/content-writing/newsletter-curator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Keys:**
    You will need an API Key for OpenAI (`OPENAI_API_KEY`) or Google Gemini. You can enter this in the UI sidebar.

## Usage

Run the Streamlit application:

```bash
streamlit run main.py
```

Open your browser to the URL displayed (usually `http://localhost:8501`).

### Workflow
1.  Enter your API Key in the sidebar.
2.  Configure your RSS feeds (defaults provided).
3.  Set your topics of interest (e.g., "AI, Rust, WebAssembly").
4.  Click **Generate Newsletter**.
5.  View the progress as the agent fetches, analyzes, and curates the content.
6.  Download the final newsletter as Markdown or HTML.

## Testing

Run the test suite with coverage:

```bash
pytest --cov=agent tests/
```

## Structure

- `main.py`: The Streamlit entry point and UI logic.
- `agent/`: Core agent logic (fetching, processing, formatting).
- `prompts/`: LangChain prompt templates.
- `config.py`: Default configuration settings.
- `tests/`: Unit tests.
