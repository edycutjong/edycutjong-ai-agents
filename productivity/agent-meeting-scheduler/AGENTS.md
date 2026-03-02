# AGENTS.md — agent-meeting-scheduler

## Overview
AI agent that finds optimal meeting times across calendars, handles timezone differences.

## Tech Stack
- **Stack:** Python/TypeScript, LangChain/LlamaIndex
- **Build:** Agent framework

## Features
- Autonomous task execution
- Tool use (API calls, file ops, web search)
- Memory for context retention
- Configurable via YAML
- Logging and audit trail
- Human-in-the-loop approval mode
- Rate limiting and cost controls
- Multiple LLM backend support

## File Structure
- `src/agent.py` — Agent definition
- `src/tools/` — Tool implementations
- `src/prompts/` — System prompts
- `config.yaml` — Configuration
- `requirements.txt`
