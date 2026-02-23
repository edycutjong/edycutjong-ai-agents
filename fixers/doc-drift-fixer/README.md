# Doc Drift Fixer

Aligns documentation with code changes.

## Features
- Connect to Git
- Analyze PR diffs
- Scan related docs
- Propose doc updates
- Verify code examples
- Check outdated links
- Comment on PR
- Commit changes

## Usage
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the agent:
    ```bash
    python agent.py
    ```

## Configuration
Set the following environment variables in a `.env` file:
- `OPENAI_API_KEY`: Your OpenAI API key.
- `GITHUB_TOKEN`: Your GitHub token (optional, for PR interaction).
