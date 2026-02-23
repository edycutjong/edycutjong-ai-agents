# AGENTS.md — Release note agent

## Overview
Release note agent — Analyze git commit range. Designed as a agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Analyze git commit range
- Group by feat/fix/chore
- Summarize changes
- Generate markdown output
- Publish to release

## Files
- requirements.txt
- main.py
- agent_config.py
- .env.example
changelog-writer/
└── AGENTS.md

## Design
- CLI-first interaction
- Verbose logging
- Modular agent definitions

