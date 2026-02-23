# AGENTS.md — Documentation generator

## Overview
Documentation generator — Parse codebase AST. Designed as a agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse codebase AST
- Generate docstrings/README
- Identify missing docs
- Update outdated docs
- Follow style guide

## Files
- requirements.txt
- main.py
- agent_config.py
- .env.example
doc-writer/
└── AGENTS.md

## Design
- CLI-first interaction
- Verbose logging
- Modular agent definitions

