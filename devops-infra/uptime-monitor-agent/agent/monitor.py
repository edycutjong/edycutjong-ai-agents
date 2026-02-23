import requests
import time
import ssl
import socket
from datetime import datetime
import re

def check_endpoint(url):
    """
    Checks an HTTP endpoint.
    Returns:
        status_code (int): HTTP status code.
        response_time (float): Response time in seconds.
        error_message (str): Error message if any.
    """
    start_time = time.time()
    try:
        response = requests.get(url, timeout=10)
        end_time = time.time()
        response_time = end_time - start_time
        return response.status_code, response_time, None
    except requests.exceptions.RequestException as e:
        end_time = time.time()
        response_time = end_time - start_time
        return 0, response_time, str(e)

def check_ssl_expiry(url):
    """
    Checks the SSL certificate expiry for a URL.
    Returns:
        days_to_expiry (int): Number of days until expiry.
        error_message (str): Error message if any.
    """
    try:
        hostname = url.split("//")[-1].split("/")[0].split(":")[0]
        port = 443

        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiry_date_str = cert['notAfter']
                # Format: 'May 20 23:59:59 2025 GMT'
                expiry_date = datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')
                days_to_expiry = (expiry_date - datetime.utcnow()).days
                return days_to_expiry, None
    except Exception as e:
        return None, str(e)

def check_custom_regex(url, regex_pattern):
    """
    Checks if the response body matches a regex pattern.
    Returns:
        matches (bool): True if matches, False otherwise.
        error_message (str): Error message if any.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content = response.text
            if re.search(regex_pattern, content):
                return True, None
            else:
                return False, f"Pattern '{regex_pattern}' not found in response."
        else:
            return False, f"HTTP Status {response.status_code}"
    except Exception as e:
        return False, str(e)
