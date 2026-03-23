# PR Review Assistant Agent

A Streamlit-powered code review assistant that analyses GitHub Pull Requests for common issues, security patterns, and best practices.

## Features
- **PR URL Input** — Paste any GitHub PR URL to fetch and analyse changes.
- **Heuristic Analysis** — Checks for TODOs, large files, hardcoded secrets, eval usage, hardcoded IPs, and missing tests.
- **Security Scanning** — Detects hardcoded passwords, API keys, tokens, and dangerous function calls.
- **Severity Badges** — Critical / Warning / Info classification.
- **Markdown Export** — Copy the structured review as a Markdown comment for GitHub.

## Usage

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Testing

```bash
pytest
```
