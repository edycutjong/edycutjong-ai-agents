# Technical Blog Reviewer

An automated AI agent that reviews technical blog posts for accuracy, code correctness, and readability.

## Features

- **Technical Accuracy Check**: Validates claims and identifies outdated info.
- **Code Verification**: Checks syntax and runs Python snippets (safely) to ensure correctness.
- **Readability Analysis**: Assesses flow, structure, and tone.
- **Comprehensive Report**: Generates a detailed report with scores and actionable feedback.
- **Premium UI**: Streamlit-based interface for easy interaction.

## Installation

1. Clone the repository.
2. Navigate to the project directory:
   ```bash
   cd apps/agents/content-writing/technical-blog-reviewer
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with your OpenAI API Key:
   ```bash
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```

## Usage

### CLI

Run the reviewer from the command line:

```bash
python main.py path/to/article.md
# OR
python main.py https://example.com/blog-post
```

Options:
- `--model`: Specify the OpenAI model (default: `gpt-4o`).
- `--output`: Save the report to a JSON file.

### UI (Streamlit)

Launch the interactive web interface:

```bash
streamlit run ui.py
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## Architecture

- `agent/core.py`: Main agent logic using LangChain.
- `agent/tools.py`: Helper tools for URL fetching and code execution.
- `prompts/system_prompts.py`: System prompts for different review personas.
- `ui.py`: Streamlit frontend.
- `main.py`: CLI entry point.
