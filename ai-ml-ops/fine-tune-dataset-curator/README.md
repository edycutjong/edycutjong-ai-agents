# Fine-Tune Dataset Curator

This application is an AI Agent designed to help you curate and format datasets for LLM fine-tuning.

## Features

- **Load Data**: Supports CSV, JSON, and JSONL formats.
- **Clean Data**: Removes empty entries and strips whitespace.
- **Deduplicate**: Removes exact duplicate entries.
- **Format**:
    - **OpenAI**: Converts to `{"messages": [...]}` JSONL format.
    - **Hugging Face**: Standardizes for datasets library.
- **Validate**: Checks structure and basic quality.
- **Split**: Train/Validation splitting.
- **Balance**: Undersample or oversample to balance categories.
- **Statistics**: Token counts and entry counts.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration**:
    -   Copy `.env.example` to `.env`.
    -   Add your `OPENAI_API_KEY`.

## Usage

Run the agent via the CLI:

```bash
python main.py "Clean my dataset at data/raw.csv and format it for OpenAI fine-tuning"
```

The agent will read the file, perform the requested actions, and provide the result or save it (depending on the implementation details and user request).

## Testing

Run the tests:

```bash
pytest tests/
```

## Structure

- `agent/`: Contains the agent definition and tools.
- `prompts/`: System prompts.
- `tests/`: Unit tests.
- `config.py`: Configuration management.
- `main.py`: Entry point.
