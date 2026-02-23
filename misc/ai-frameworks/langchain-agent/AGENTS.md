# AGENTS.md — LangChain Agent

## Overview
An AI research agent that can search the web, summarize documents, and answer complex questions using LangChain and OpenAI. Runs as a CLI tool.

## Tech
- Python 3.12, LangChain, OpenAI API
- FAISS for vector storage
- Rich for terminal UI

## Features
- Conversational AI with memory (chat history)
- Web search tool (DuckDuckGo integration)
- Document Q&A: load PDF/TXT, chunk, embed, query
- Multi-step reasoning with chain-of-thought
- Tool use: calculator, web search, file reader
- Streaming responses in terminal
- Export conversation history as markdown
- Configurable model (gpt-4, gpt-3.5-turbo)

## Files
- `agent.py` — Main agent setup with tools and memory
- `tools/` — Custom tool definitions (search, calculator, file_reader)
- `chains/` — Custom chains (summarize, qa, research)
- `vectorstore.py` — FAISS document embedding and retrieval
- `cli.py` — Rich terminal interface
- `config.py` — Model and API configuration
- `requirements.txt`
- `.env.example` — OPENAI_API_KEY

## Commands
```bash
pip install -r requirements.txt
python cli.py            # interactive mode
python cli.py --query "your question"
python cli.py --file document.pdf --query "summarize this"
pytest
```
