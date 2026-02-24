# Langchain Agent

## Overview
An AI research agent that can search the web, summarize documents, and answer complex questions using LangChain and OpenAI. Runs as a CLI tool.

## Tech
- Python 3.10+
- LangChain
- OpenAI API

## Features
- Conversational AI with memory (chat history)
- Web search tool (DuckDuckGo integration)
- Document Q&A: load PDF/TXT, chunk, embed, query
- Multi-step reasoning with chain-of-thought
- Tool use: calculator, web search, file reader
- Streaming responses in terminal
- Export conversation history as markdown
- Configurable model (gpt-4, gpt-3.5-turbo)

## File Structure
- `README.md` — Documentation
- `agent.py` — Agent
- `chains/` — Chains module
- `cli.py` — Cli
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `tools/` — Tools module
- `vectorstore.py` — Vectorstore

## API Keys
- `OPENAI_API_KEY` — Required

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
