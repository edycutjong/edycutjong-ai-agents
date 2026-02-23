# AGENTS.md — code-review-automator

## Overview
AI agent that connects to GitHub PRs and provides first-pass code review.

## Tech
- **Runtime:** Python 3.11+ or Node.js
- **AI:** OpenAI API / Anthropic API / Gemini
- **Framework:** LangChain or custom loop
- **Interface:** CLI or Streamlit

## Features
- Fetch PR diffs\n- Analyze logic/security/style\n- Post comments on specific lines\n- Summary generation\n- Customizable guidelines\n- Ignore patterns\n- Detect hallucinations checks\n- Integration with CI

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings

## Commands
python3 main.py
