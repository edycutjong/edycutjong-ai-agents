# Markdown to PDF Agent

A premium CLI application to convert styled Markdown documents into high-quality PDFs. Features AI-powered content polishing, customizable themes, and batch processing.

## Features

- **Premium PDF Output:** Styled with CSS themes (Default, Dark, Minimal).
- **AI Integration:** Polish grammar, structure, and tone using OpenAI/Gemini (via LangChain).
- **Rich CLI:** Beautiful terminal interface with progress bars and interactive menus.
- **Batch Processing:** Convert multiple files at once.
- **Frontmatter Support:** Parse metadata for custom titles and authors.

## Installation

1.  Navigate to the project directory:
    ```bash
    cd apps/agents/file-conversion/markdown-to-pdf-agent
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  (Optional) Set up your `.env` file for AI features:
    ```bash
    cp .env.example .env
    # Add your OPENAI_API_KEY
    ```

## Usage

Run the agent:

```bash
python main.py
```

Follow the interactive menu to select files and themes.

## File Structure

- `agent/`: Core logic (Parser, Converter, AI Editor).
- `themes/`: CSS themes for PDF generation.
- `input/`: Default folder for input Markdown files.
- `output/`: Default folder for generated PDFs.
- `tests/`: Unit tests.

## Testing

Run tests with `pytest`:

```bash
pytest
```
