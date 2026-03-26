# Notification Router

Smart notification routing agent that analyzes message urgency and routes alerts to the appropriate channel (email, Slack, SMS, push).

## Features
- Urgency classification (critical/high/medium/low)
- Multi-channel routing rules
- Quiet hours & DND respect
- Escalation chains
- Deduplication logic
- Template-based message formatting
- Delivery confirmation tracking
- Rule builder CLI

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
