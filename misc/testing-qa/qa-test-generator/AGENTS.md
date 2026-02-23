# AGENTS.md — qa-test-generator

## Overview
Agent that reads features/code and generates Cypress/Playwright tests.

## Tech Stack
- **Runtime:** Python 3.11+ or Node.js
- **AI:** OpenAI API / Anthropic API / Gemini
- **Framework:** LangChain or custom loop
- **Interface:** CLI or Streamlit

## Features
- Parse UI components\n- Generate test scenarios\n- Write executable test code\n- Mock API responses\n- Self-healing tests (update selectors)\n- Integration with test runner\n- Coverage analysis\n- Edge case generation

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings

## Design Notes
Test suite dashboard.

## Commands
python3 main.py
