# AGENTS.md — Unit test writer

## Overview
Unit test writer — Analyze function signature. Designed as a agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Analyze function signature
- Generate happy path tests
- Generate edge case tests
- Mock dependencies
- Run generated tests

## Files
- requirements.txt
- main.py
- agent_config.py
- .env.example
test-generator/
└── AGENTS.md

## Design
- CLI-first interaction
- Verbose logging
- Modular agent definitions

