# Habit Coach

Tracks daily habits, analyzes patterns, provides motivational nudges and streak tracking. Designed as an AI agents project.

## Features
- Define trackable habits
- Log daily completions
- Calculate streaks and chains
- Analyze completion patterns
- Generate motivational reminders
- Visualize habit heatmaps
- Identify best/worst days
- Generate weekly progress reports

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Copy `.env.example` to `.env` and add your OpenAI API Key.
    ```bash
    cp .env.example .env
    ```

3.  **Run the Application**:
    ```bash
    streamlit run main.py
    ```

## Testing
Run tests with:
```bash
pytest tests/
```
