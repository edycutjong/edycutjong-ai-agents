# Standup Report Generator 📋

Generate daily/weekly standup reports with blocker tracking, mood indicators, and tags.

## Quick Start

```bash
pip install -r requirements.txt
python main.py add --author "Alice" --yesterday "Fixed bug" --today "Deploy;Write tests" --blockers "Waiting on API key" --mood good
python main.py daily
python main.py weekly
python main.py blockers
python -m pytest tests/ -v
```
