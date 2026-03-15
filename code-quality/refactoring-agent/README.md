# Refactoring Agent

AI agent that identifies code smells, suggests refactoring patterns, and generates pull requests.

## Features
1. Core functionality as described above
2. Configurable via environment variables
3. Structured output parsing
4. Rate limiting and retry logic
5. Logging and audit trail
6. Dry-run mode

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```
2. Build the project:
   ```bash
   npm run build
   ```

## Usage

Set the required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API Key
- `GITHUB_TOKEN`: Your GitHub personal access token

Run the agent:
```bash
npm start <owner> <repo> <path/to/file>
```

## Dry Run Mode
To run without making actual pull requests, set `DRY_RUN=true`.
