# Incident Responder Agent

An AI-powered agent that monitors logs, detects anomalies, and generates incident reports with Root Cause Analysis (RCA).

## Features
- Real-time log monitoring (simulated).
- Anomaly detection using LLMs (LangChain).
- Automated incident reporting (Markdown & PDF).
- Slack & PagerDuty integration (simulated).
- Premium Streamlit UI.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file with your OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-...
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
   Or run the CLI:
   ```bash
   python main.py
   ```

## Testing
Run tests with pytest:
```bash
pytest tests/
```
