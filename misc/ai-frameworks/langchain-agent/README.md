# LangChain Research Agent

An AI research agent that can search the web, summarize documents, and answer complex questions using LangChain and OpenAI. Runs as a CLI tool.

## Features

- 💬 **Conversational AI** with chat history and memory
- 🔍 **Web Search** via DuckDuckGo integration
- 📄 **Document Q&A** — load PDF/TXT, chunk, embed, query
- 🧮 **Calculator** — safe math evaluation
- 📎 **File Reader** — read text and PDF files
- 🧠 **Multi-step Reasoning** with chain-of-thought
- 💾 **Export** conversation history as markdown

## Setup

1. Copy `.env.example` to `.env` and add your OpenAI API key
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
# Interactive chat mode
python cli.py

# Single query
python cli.py --query "What are the latest AI trends?"

# Document Q&A
python cli.py --file document.pdf --query "Summarize this"

# Interactive with loaded document
python cli.py --file notes.txt
```

## Architecture

```
├── cli.py              # Rich terminal interface
├── agent.py            # Agent setup with tools & memory
├── config.py           # Model & API configuration
├── vectorstore.py      # FAISS document embedding
├── tools/
│   ├── search.py       # DuckDuckGo web search
│   ├── calculator.py   # Safe math evaluator
│   └── file_reader.py  # Text/PDF file reader
├── chains/
│   ├── summarize.py    # Document summarization
│   ├── qa.py           # Context-based Q&A
│   └── research.py     # Research analysis
└── exports/            # Saved conversations
```

## Interactive Commands

| Command | Description |
|---------|-------------|
| `/search <query>` | Web search |
| `/export` | Save chat history |
| `/clear` | Clear memory |
| `/quit` | Exit |
