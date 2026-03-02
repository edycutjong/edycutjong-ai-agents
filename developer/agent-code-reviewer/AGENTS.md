# AGENTS.md — agent-code-reviewer

## Overview
AI agent that reviews code changes — checks style, logic, security, and suggests improvements.

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
