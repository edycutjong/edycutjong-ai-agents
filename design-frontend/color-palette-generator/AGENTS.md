# AGENTS.md — Color Palette Generator

## Overview
Generates harmonious color palettes from images, brand descriptions, or mood keywords. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Generate palettes from text descriptions
- Extract colors from images
- Create complementary/analogous schemes
- Generate CSS custom properties
- Create Tailwind color configs
- Check WCAG contrast ratios
- Export as ASE/JSON/CSS
- Support dark/light mode variants

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
