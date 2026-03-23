# A11Y Fixer Agent

An AI-powered Python agent that scans HTML for accessibility (WCAG) issues and auto-generates fixes including alt text, ARIA labels, and contrast improvements.

## Features

- Scan HTML for WCAG violations
- Auto-generate alt text for images using local LLM integration
- Add missing ARIA labels and roles
- Fix heading hierarchy issues
- Detect color contrast failures (passes AA/AAA checks)
- Generate a beautiful styled accessibility audit report

## Tech Stack

- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Dependencies:** BeautifulSoup4, pytest

## Setup

1. Clone the repository.
2. Setup a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_key_here
   ```

## Usage

Run the static analysis and generate an accessibility report for an HTML file:

```bash
python -m agent.main path/to/index.html --out report.html
```

To attempt auto-fixing the file in place (experimental):

```bash
python -m agent.main path/to/index.html --fix
```

## Testing

Run unit tests via Pytest to verify utility functions and standard issues logic:

```bash
pytest tests/
```

## Authors
Jules Autonomous Web Builder
