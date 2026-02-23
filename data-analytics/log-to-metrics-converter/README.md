# Log to Metrics Converter

An AI-powered agent application that transforms unstructured application logs into structured metrics and dashboard configurations.

## Features

- **Log Parsing**: Uses LLM (or regex fallback) to parse unstructured logs into structured JSON.
- **Metric Extraction**: Identifies key metrics (latency, error rates, throughput) from parsed logs.
- **Prometheus Configuration**: Automatically generates Prometheus scrape configs and recording rules.
- **Grafana Dashboards**: Generates ready-to-import Grafana dashboard JSON models.
- **Documentation**: Auto-generates markdown documentation for the discovered metrics.
- **Premium UI**: Built with Streamlit for a seamless user experience.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables (optional for Mock Mode):
   Create a `.env` file:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the application:

```bash
python main.py
```
Or:
```bash
streamlit run main.py
```

### Workflow

1. **Input Logs**: Paste your logs or upload a file in the UI.
2. **Analyze**: Click "Analyze Logs" to parse them.
3. **Explore**:
   - **Parsed Data**: View the structured log table.
   - **Metrics**: See the suggested metrics extracted from the logs.
   - **Prometheus**: Copy the generated Prometheus configuration.
   - **Grafana**: Download the Grafana dashboard JSON.
   - **Documentation**: Read the auto-generated metric docs.

## Testing

Run the test suite:

```bash
pytest tests/
```

## Structure

- `agent/`: Core agent logic (Parsing, Metric Extraction, Generation).
- `prompts/`: System prompts for the AI.
- `tests/`: Unit tests.
- `main.py`: Streamlit application entry point.
- `config.py`: Configuration settings.
