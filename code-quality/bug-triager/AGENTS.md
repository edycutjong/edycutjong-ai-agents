# AGENTS.md — Issue management agent

## Overview
Issue management agent — Read new GitHub issues. Designed as a agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Read new GitHub issues
- Label based on content
- Assign to maintainers
- Check for duplicates
- Reply with template

## Files
- requirements.txt
- main.py
- agent_config.py
- .env.example
bug-triager/
└── AGENTS.md

## Design
- CLI-first interaction
- Verbose logging
- Modular agent definitions

