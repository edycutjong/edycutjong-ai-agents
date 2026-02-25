import requests
import time
import ssl
import socket
from datetime import datetime
import re
import ipaddress
from urllib.parse import urlparse, urljoin

def validate_url(url):
    """
    Validates a URL for SSRF protection.
    Raises ValueError if validation fails.
    """
    try:
        parsed = urlparse(url)
    except Exception as e:
         raise ValueError(f"Invalid URL format: {e}")

    if parsed.scheme not in ('http', 'https'):
        raise ValueError(f"Invalid scheme: {parsed.scheme}. Only http and https are allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Invalid hostname.")

    try:
        # Resolve hostname to IPs (IPv4 and IPv6)
        # 0 = any family, SOCK_STREAM = TCP
        addr_infos = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)

        for family, type, proto, canonname, sockaddr in addr_infos:
            ip_str = sockaddr[0]
            ip_obj = ipaddress.ip_address(ip_str)

            # Check for private/reserved/loopback IPs
            if (ip_obj.is_private or
                ip_obj.is_loopback or
                ip_obj.is_link_local or
                ip_obj.is_multicast or
                ip_obj.is_reserved or
                ip_obj.is_unspecified):
                raise ValueError(f"Access to local/private resource {ip_str} is denied.")

    except socket.gaierror:
        raise ValueError(f"Could not resolve hostname: {hostname}")

def safe_request(method, url, timeout=10, **kwargs):
    """
    Makes a safe HTTP request, validating each redirect.
    """
    current_url = url
    max_redirects = 5

    for _ in range(max_redirects + 1):
        validate_url(current_url)

        try:
            # We must disable automatic redirects to validate each step
            response = requests.request(method, current_url, allow_redirects=False, timeout=timeout, **kwargs)
        except requests.exceptions.RequestException as e:
            raise e

        if response.is_redirect:
            location = response.headers.get('Location')
            if not location:
                return response

            # Handle relative redirects
            current_url = urljoin(current_url, location)
            continue
        else:
            return response

    raise requests.exceptions.TooManyRedirects("Exceeded maximum redirect limit")

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
        response = safe_request('GET', url, timeout=10)
        end_time = time.time()
        response_time = end_time - start_time
        return response.status_code, response_time, None
    except (requests.exceptions.RequestException, ValueError) as e:
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
        validate_url(url)
        parsed = urlparse(url)
        hostname = parsed.hostname
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
        response = safe_request('GET', url, timeout=10)
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
