# AGENTS.md — resume-tailor-agent

## Overview
Agent that tailors your resume/CV for specific job descriptions.

## Tech Stack
- **Runtime:** Python 3.11+ or Node.js
- **AI:** OpenAI API / Anthropic API / Gemini
- **Framework:** LangChain or custom loop
- **Interface:** CLI or Streamlit

## Features
- Ingest master resume\n- Ingest job description\n- Rewrite bullet points\n- Optimize keywords\n- Generate cover letter\n- Formatting adjustment\n- PDF export\n- Version tracking

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings

## Design Notes
Split screen: Job vs Resume.

## Commands
python3 main.py
