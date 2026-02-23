# Dependency Bloat Reducer

A premium CLI tool to analyze, visualize, and reduce dependency bloat in JavaScript/TypeScript projects.

## Features
- **Bundle Size Analysis**: Fetches size data from Bundlephobia.
- **Unused Dependency Detection**: Scans source code and scripts.
- **Duplicate Package Check**: Analyzes lockfiles.
- **AI Suggestions**: Recommendations for lighter alternatives (requires OPENAI_API_KEY).
- **Interactive Report**: Generates a beautiful HTML dashboard with Treemaps.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the agent:
   ```bash
   python agent.py /path/to/your/project
   ```

3. View the generated report in `dependency-report/report.html`.

## Environment Variables
- `OPENAI_API_KEY`: Required for AI suggestions.
