# Uptime Monitor Agent

An AI-powered uptime monitoring agent that polls HTTP endpoints, detects downtime, checks SSL expiry, and provides diagnostic context using LangChain.

## Features

- Polls configurable endpoints at regular intervals.
- Checks HTTP status codes and response times.
- Detects SSL certificate expiry.
- Sends alerts via Webhook (e.g., Discord/Slack) and Email.
- Generates AI-powered diagnostic context for failures.
- Provides a premium Streamlit dashboard for real-time monitoring and history.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/uptime-monitor-agent.git
    cd uptime-monitor-agent
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    - Copy `.env.example` to `.env`.
    - Fill in the required values (OpenAI API key, endpoints, email settings, webhook URL).

## Usage

### Run the Monitor Agent

To start the background monitoring process:

```bash
python main.py
```

### Run the Dashboard

To view the monitoring dashboard:

```bash
streamlit run dashboard.py
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
