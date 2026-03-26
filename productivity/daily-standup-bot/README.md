# Daily Standup Bot

Async daily standup collection agent that gathers team updates, identifies blockers, and generates formatted standup summaries.

## Features
- Async standup collection via CLI
- Yesterday/Today/Blockers format
- Team summary generation
- Blocker escalation detection
- Trend analysis (recurring blockers)
- Attendance tracking
- Historical standup archive
- Export as Slack/email digest

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
