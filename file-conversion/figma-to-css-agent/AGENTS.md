# AGENTS.md — Figma to CSS Agent

## Overview
Extracts design properties from Figma export files and generates production CSS. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse Figma JSON exports
- Extract layout properties (flex, grid)
- Generate CSS classes
- Convert colors to CSS variables
- Handle responsive breakpoints
- Generate component CSS modules
- Support SCSS/CSS-in-JS output
- Create design system starter

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings
- `requirements.txt`: Dependencies
- `tests/`: Test files

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
