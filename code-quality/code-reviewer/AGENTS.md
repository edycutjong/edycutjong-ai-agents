# AGENTS.md — PR review agent

## Overview
PR review agent — Fetch PR diff from GitHub. Designed as a agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Fetch PR diff from GitHub
- Analyze code quality/bugs
- Post comment suggestions
- Check style guide
- Security scan

## Files
- requirements.txt
- main.py
- agent_config.py
- .env.example
code-reviewer/
└── AGENTS.md

## Design
- CLI-first interaction
- Verbose logging
- Modular agent definitions

