# Research Agent

Autonomous agent that researches a topic using web search and compiles structured reports.

## Features
- Accept research topic as input
- Multi-query web search strategy
- Source credibility scoring
- Structured report generation (intro, findings, sources)
- Key findings extraction
- Citation management
- Markdown and PDF output
- Iterative depth research
- Configurable search depth
- Rate-limited API calls

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
