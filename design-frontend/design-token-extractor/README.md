# Design Token Extractor Agent

An AI-powered agent that extracts design tokens (colors, fonts, spacing) from design specs (Figma JSON, Markdown) and generates CSS, SCSS, Tailwind config, and JSON tokens.

## Features
- Parse Design Specs (Markdown/JSON)
- Extract Tokens using LLM
- Generate CSS Variables
- Generate SCSS Variables
- Generate Tailwind Config
- Generate Design Tokens (W3C format)
- Premium Streamlit UI

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up `.env` with `OPENAI_API_KEY`.
3. Run the app:
   ```bash
   streamlit run main.py
   ```
