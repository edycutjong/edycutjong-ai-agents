# AI Code Review Automator

An AI-powered agent that connects to GitHub Pull Requests and provides intelligent, first-pass code reviews. It analyzes logic, security, and style, offering constructive feedback and code suggestions.

## Features

- **Automated Code Analysis**: Uses OpenAI (GPT-3.5/4) to review code changes.
- **Multi-Category Focus**: Reviews for Logic, Security, Style, Performance, and Best Practices.
- **Hallucination Checks**: Verifies that suggested comments apply to actual lines in the diff.
- **Premium UI**: Modern, dark-themed dashboard built with Streamlit.
- **CLI Support**: Command-line interface for CI/CD integration.
- **GitHub Integration**: Fetches PR diffs and posts comments directly to GitHub.
- **Custom Guidelines**: Support for project-specific review guidelines.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```

   - `OPENAI_API_KEY`: Your OpenAI API Key.
   - `GITHUB_TOKEN`: A GitHub Personal Access Token (PAT) with `repo` scope.

## Usage

### Web Dashboard (Streamlit)

Launch the interactive UI:
```bash
streamlit run main.py
```

1. Enter your API keys (if not in `.env`).
2. Paste the GitHub Pull Request URL.
3. Configure review settings (focus categories, custom guidelines).
4. Click "Start Review".
5. Review the summary and detailed findings.
6. Click "Post to GitHub" to submit the review.

### CLI (Command Line Interface)

Run the automator from the terminal, useful for CI/CD pipelines:

```bash
python3 cli.py --repo owner/repo --pr 123 --post
```

**Options:**
- `--repo`: GitHub repository name (e.g., `facebook/react`).
- `--pr`: Pull Request number.
- `--token`: GitHub Token (optional if set in env).
- `--api-key`: OpenAI API Key (optional if set in env).
- `--post`: If set, comments will be posted to GitHub.
- `--focus`: Comma-separated categories (default: Logic,Security,Style).
- `--guidelines`: Custom review guidelines string.

## Testing

Run the unit tests:
```bash
python3 tests/test_reviewer.py
```

## Project Structure

- `agent/`: Core logic (GitHub client, Reviewer).
- `prompts/`: System prompts for the AI.
- `main.py`: Streamlit application entry point.
- `cli.py`: CLI entry point.
- `config.py`: Configuration management.

## CI Integration Example (GitHub Actions)

You can run this tool as a step in your GitHub Actions workflow:

```yaml
steps:
  - uses: actions/checkout@v3
  - name: Set up Python
    uses: actions/setup-python@v4
    with:
      python-version: '3.11'
  - name: Install Dependencies
    run: pip install -r apps/agents/code-review-automator/requirements.txt
  - name: Run Code Review
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    run: |
      python3 apps/agents/code-review-automator/cli.py \
        --repo ${{ github.repository }} \
        --pr ${{ github.event.pull_request.number }} \
        --post
```
