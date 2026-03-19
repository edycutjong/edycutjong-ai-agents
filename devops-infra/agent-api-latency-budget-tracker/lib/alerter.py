import httpx
from typing import Dict, Any

def send_alert(webhook_url: str, message: str) -> bool:
    """
    Sends an alert to a webhook.
    """
    if not webhook_url:
        return False
        
    payload = {"text": message}
    try:
        response = httpx.post(webhook_url, json=payload, timeout=5.0)
        return response.status_code < 400
    except Exception:
        return False
