# Infrastructure Cost Analyzer

An AI-powered agent to analyze cloud billing data, identify waste, and suggest cost-saving opportunities.

## Features
- **Data Ingestion:** Parse billing CSVs from AWS, GCP, Azure, or Generic formats.
- **Waste Detection:** Identify unused resources (e.g., unattached IPs, old snapshots) and low-utilization instances.
- **Right-Sizing:** Suggest instance type modifications based on utilization heuristics.
- **AI Insights:** Generates natural language reports using LLMs (OpenAI) summarizing the financial health of your infrastructure.
- **Premium UI:** Interactive Dashboard with charts and metrics built with Streamlit and Plotly.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration:**
   - Create a `.env` file in this directory (optional, for real AI analysis).
   - Add your OpenAI API Key:
     ```
     OPENAI_API_KEY=sk-...
     ```
   - If no key is provided, the agent runs in **Mock Mode**, providing simulated insights.

## Running the Application

```bash
streamlit run main.py
```

## Running Tests

```bash
pytest tests/
```

## Usage
1. Launch the app.
2. Select your Cloud Provider in the sidebar.
3. Upload a billing CSV file (Samples available in `data/`).
4. View the **Dashboard** for metrics and charts.
5. Go to the **AI Insights** tab and click "Generate AI Report" to get a summary.

## Sample Data
Sample CSV files for AWS and GCP are located in the `data/` directory for testing purposes.
