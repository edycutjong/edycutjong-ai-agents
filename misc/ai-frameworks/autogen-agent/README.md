# AutoGen Agent

A conversational AI system with multiple agents that can write code, debug, and execute tasks collaboratively. Built with Microsoft AutoGen.

## Features

- 🤖 **AssistantAgent** — Plans and writes clean Python code
- 👤 **UserProxyAgent** — Executes code and provides feedback
- 💬 **GroupChat** — Multi-agent discussion for complex problems
- 🔧 **Auto-debugging** — Retry with error feedback loops
- 📋 **Preset Tasks** — Code generation, data analysis, math problems
- 📄 **Conversation Logging** — Export chats as JSON

## Setup

1. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-...
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
# Run a custom task
python main.py --task "Write a Python script that generates prime numbers"

# Use a preset task
python main.py --preset fibonacci

# Use group chat mode (3 agents)
python main.py --group --task "Build a web scraper and analyze the data"

# Attach a file for context
python main.py --task "Analyze this data" --file data.csv

# List available presets
python main.py --list-presets
```

## Preset Tasks

| Preset | Description |
|--------|-------------|
| `fibonacci` | Generate Fibonacci sequence |
| `data_analysis` | Sample data analysis with pandas |
| `web_scraper` | Scrape Hacker News top stories |
| `api_server` | Build a FastAPI REST API |
| `math_solver` | Find happy primes |

## Architecture

```
├── main.py              # Entry point & CLI
├── config.py            # Model & execution settings
├── agents/
│   ├── assistant.py     # Code-writing AI agent
│   ├── user_proxy.py    # Code execution proxy
│   └── group_chat.py    # Multi-agent orchestration
├── tasks/
│   └── __init__.py      # Predefined task library
├── workspace/           # Code execution sandbox
└── logs/                # Conversation logs (JSON)
```

## Configuration

Edit `config.py` to customize:
- **Model** — Switch between GPT-4o, GPT-4o-mini, etc.
- **Temperature** — Adjust creativity (0.0–1.0)
- **Execution** — Enable Docker sandbox
- **Input Mode** — ALWAYS, TERMINATE, or NEVER
