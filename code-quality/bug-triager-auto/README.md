# Auto Bug Triager

An AI-powered bug triage agent with a premium Streamlit UI.

## Features
- **Automated Triage**: Analyzes new issues for severity, team routing, and sentiment.
- **Duplicate Detection**: Identifies similar existing issues.
- **Fix Suggestions**: Generates potential fix strategies and file locations using AI.
- **Stale Issue Management**: Automatically flags old inactive issues.
- **Premium Dashboard**: Visualizes issue statistics and team load.

## Tech Stack
- **Python 3.11+**
- **Streamlit**: Interactive web interface.
- **LangChain & OpenAI**: AI reasoning and analysis.
- **Altair**: Data visualization.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration**:
    Create a `.env` file in this directory with your OpenAI API key:
    ```env
    OPENAI_API_KEY=sk-your-key-here
    DEMO_MODE=False  # Set to True to run without API keys (mock mode)
    ```

3.  **Run the App**:
    ```bash
    streamlit run main.py
    ```

## Usage
- **Dashboard**: View high-level metrics and charts.
- **Issue Tracker**: Filter and manage existing issues.
- **New Issue**: Submit a bug report and watch the AI triage it in real-time.

## Testing
Run the test suite:
```bash
pytest tests/
```
