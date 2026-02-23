# Spreadsheet Formula Writer Agent

A powerful AI-powered tool to convert natural language queries into complex Excel and Google Sheets formulas.

## Features

- **Natural Language Parsing**: Understands complex English instructions.
- **Dual Support**: Generates formulas for both Excel and Google Sheets.
- **Advanced Logic**: Supports nested IFs, XLOOKUP, LAMBDA, LET, and dynamic arrays.
- **Explanations**: Provides step-by-step logic breakdown for every formula.
- **Premium UI**:
  - **Web Interface**: Interactive Streamlit app with history and configuration.
  - **CLI**: Rich terminal user interface for quick tasks.

## Installation

1. Navigate to the project directory:
   ```bash
   cd apps/agents/data-analytics/spreadsheet-formula-writer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment:
   - Create a `.env` file based on `.env.example`.
   - Add your `OPENAI_API_KEY`.

## Usage

### Web Interface (Recommended)

Run the Streamlit app for a premium graphical experience:

```bash
streamlit run app.py
```

Features:
- Sidebar configuration for Target Application and Model.
- History of generated formulas.
- Copy-paste ready code blocks.

### Command Line Interface

Run the CLI for quick access:

```bash
python main.py "Sum column A if column B is 'Pending'"
```

Options:
- `--target` / `-t`: Target application (`Excel` or `Google Sheets`). Default: `Excel`.
- `--model` / `-m`: OpenAI model (`gpt-4o`, `gpt-3.5-turbo`). Default: `gpt-4o`.

Interactive Mode:
```bash
python main.py
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## Project Structure

- `app.py`: Streamlit web application.
- `main.py`: CLI entry point.
- `agent/`: Core agent logic.
- `prompts/`: System prompts and templates.
- `tests/`: Unit tests.
