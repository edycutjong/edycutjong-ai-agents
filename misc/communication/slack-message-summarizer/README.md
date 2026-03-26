# Slack Message Summarizer

Agent that digests long Slack channels into concise summaries, extracting key decisions, action items, and important mentions.

## Features
- Channel history ingestion
- Thread-aware summarization
- Action item extraction
- Decision tracking
- Mention & reaction analysis
- Daily/weekly digest generation
- Keyword-based filtering
- Export as markdown report

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
