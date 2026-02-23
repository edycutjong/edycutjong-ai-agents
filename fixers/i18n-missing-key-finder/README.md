# i18n Missing Key Finder Agent

A powerful CLI tool to find missing i18n translation keys in your codebase.

## Features
- Scans source code for translation keys (e.g., `t('key')`).
- Compares found keys against locale files (JSON).
- Identifies missing and unused keys.
- Auto-translates missing keys using OpenAI (via LangChain).
- Generates a report.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the agent:
   ```bash
   python agent.py --source ./src --locale ./locales --lang en
   ```

## Options
- `--source`: Path to source code directory.
- `--locale`: Path to locale files directory.
- `--lang`: Target language code (default: en).
- `--auto-translate`: Enable auto-translation for missing keys.

## Development
Run tests:
```bash
pytest
```
