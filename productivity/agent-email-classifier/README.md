# Email Classifier

AI agent that classifies and prioritizes incoming emails — urgent, actionable, FYI, spam.

## Features
- Autonomous task execution
- Tool use (API calls, file ops, web search)
- Memory for context retention
- Configurable via YAML
- Logging and audit trail
- Human-in-the-loop approval mode
- Rate limiting and cost controls
- Multiple LLM backend support

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
