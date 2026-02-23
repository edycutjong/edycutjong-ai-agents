# Paper Summarizer Agent

An AI-powered research assistant for summarizing papers, generating reading lists, and batch processing.

## Features
- **PDF Summarization**: Upload a PDF and get abstract, methodology, plain language summary, key findings, and citations.
- **Visual Summary**: Generates a Mermaid.js mindmap of the paper's concepts.
- **Batch Processing**: Summarize all PDFs in a directory.
- **Reading List**: Generate a reading list based on a research topic.
- **Premium UI**: Built with Streamlit for a user-friendly experience.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   Copy `.env.example` to `.env` and add your OpenAI API key.
   ```bash
   cp .env.example .env
   ```

## Usage

### Web UI (Recommended)
Run the Streamlit app:
```bash
streamlit run app.py
```

### CLI
Run the CLI tool:
```bash
# Summarize a single file
python main.py summarize path/to/paper.pdf --visual

# Batch process a directory
python main.py batch path/to/directory

# Generate a reading list
python main.py reading-list "Deep Learning"
```

## Testing
Run tests with coverage:
```bash
pytest --cov=. tests/
```
