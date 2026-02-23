# CrewAI Research Agent

A multi-agent crew that collaborates to research topics, write reports, and generate insights. Uses CrewAI for agent orchestration.

## Agents

| Agent | Role | Responsibility |
|-------|------|----------------|
| 🔍 **Researcher** | Senior Research Analyst | Gathers data, statistics, and expert opinions |
| ✍️ **Writer** | Senior Content Writer | Synthesizes research into structured markdown |
| 📝 **Editor** | Senior Editor | Reviews accuracy, clarity, and formatting |

## Setup

1. Copy `.env.example` to `.env` and add your OpenAI API key
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
# Research a topic
python cli.py --topic "AI trends 2025"

# Show agent reasoning
python cli.py --topic "renewable energy" --verbose

# Don't save the report to file
python cli.py --topic "market analysis" --no-save
```

## Architecture

```
├── cli.py               # CLI entry point with Rich output
├── crew.py              # Crew orchestration (agents + tasks)
├── agents/
│   ├── researcher.py    # Research agent
│   ├── writer.py        # Writing agent
│   └── editor.py        # Editing agent
├── tools/
│   ├── web_search.py    # Web search tool (simulated)
│   └── summarize.py     # Text summarization tool
└── reports/             # Generated reports (markdown)
```

## Output

Reports are saved as markdown files in `reports/` with timestamps. Each report includes:
- Executive Summary
- Key Findings
- Detailed Analysis
- Trends & Predictions
- Actionable Insights
