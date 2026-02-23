# Webhook Tester 🪝

Capture, inspect, and replay webhook requests. Generate curl commands and Python snippets from captured payloads.

## Features

- **Capture Webhooks** — Log incoming requests with headers, body, query params
- **Inspect Requests** — View full request details
- **Replay Requests** — Send captured requests to any target URL
- **Code Generation** — Auto-generate curl commands and Python snippets
- **Filter & Search** — Filter by HTTP method or path
- **Export** — JSON and Markdown export
- **No External Dependencies** — Pure Python, stdlib only

## Quick Start

```bash
pip install -r requirements.txt

# Manually capture a request
python main.py capture --method POST --path /api/hook --body '{"event":"test"}'

# List captured requests
python main.py list
python main.py list --method POST

# Show details
python main.py show <request-id>

# Generate replay code
python main.py curl <request-id>
python main.py python <request-id>

# Replay to target
python main.py replay <request-id> https://httpbin.org/post

# Export
python main.py export --format markdown
python main.py export --format json

# Clear
python main.py clear
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
webhook-tester/
├── main.py          # CLI with 8 subcommands
├── config.py        # Settings
├── requirements.txt
├── agent/
│   ├── storage.py   # Request capture + JSON storage
│   └── replay.py    # HTTP replay + code generation
└── tests/
    └── test_webhook.py  # 21 tests
```
