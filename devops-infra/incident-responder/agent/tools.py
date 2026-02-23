import os
import requests
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_slack_alert(message: str, webhook_url: str = None) -> bool:
    """Simulates sending a Slack alert."""
    if not webhook_url:
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        logger.warning("Slack Webhook URL not configured. Alert simulation only.")
        print(f"[SLACK SIMULATION] Alert Sent: {message}")
        return True

    try:
        response = requests.post(webhook_url, json={"text": message})
        response.raise_for_status()
        logger.info("Slack alert sent successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to send Slack alert: {e}")
        return False

def trigger_pagerduty_incident(summary: str, severity: str, api_key: str = None) -> bool:
    """Simulates triggering a PagerDuty incident."""
    if not api_key:
        api_key = os.getenv("PAGERDUTY_API_KEY")

    if not api_key:
        logger.warning("PagerDuty API Key not configured. Incident simulation only.")
        print(f"[PAGERDUTY SIMULATION] Incident Triggered: [{severity}] {summary}")
        return True

    # Real implementation would use PD API
    logger.info(f"PagerDuty incident triggered via API (mocked): {summary}")
    return True
