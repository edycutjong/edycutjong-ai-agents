# AGENTS.md — AutoGen Agent

## Overview
A conversational AI system with multiple agents that can write code, debug, and execute tasks collaboratively. Built with Microsoft AutoGen.

## Tech
- Python 3.12, AutoGen, OpenAI API
- Docker (optional, for code execution sandbox)

## Features
- AssistantAgent: plans and writes code
- UserProxyAgent: executes code and provides feedback
- GroupChat: multi-agent discussion for complex problems
- Code execution sandbox (Docker or local)
- Automated debugging: retry with error feedback
- Task types: code generation, data analysis, math problems
- Conversation logging and export
- Configurable agent personalities and system prompts

## Files
- `main.py` — Agent setup and conversation flow
- `agents/assistant.py` — AssistantAgent configuration
- `agents/user_proxy.py` — UserProxyAgent with code execution
- `agents/group_chat.py` — Multi-agent groupchat setup
- `config.py` — Model and execution settings
- `tasks/` — Example task definitions
- `requirements.txt`
- `.env.example` — OPENAI_API_KEY

## Commands
```bash
pip install -r requirements.txt
python main.py --task "Write a Python script that..."
python main.py --task "Analyze this CSV data" --file data.csv
pytest
```
