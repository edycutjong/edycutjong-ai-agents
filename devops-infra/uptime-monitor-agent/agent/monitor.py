import requests
import time
import ssl
import socket
from datetime import datetime
import re
from urllib.parse import urlparse, urljoin
import ipaddress

def is_safe_ip(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str)
        # Check if the IP is a global, routable IP address
        if ip.is_loopback or ip.is_private or ip.is_multicast or ip.is_link_local or ip.is_reserved or ip.is_unspecified:
            return False
        # Also catch 0.0.0.0, 255.255.255.255 explicitly if not caught above
        if str(ip) in ['0.0.0.0', '255.255.255.255']:
            return False
        return True
    except ValueError:
        return False

def validate_url(url):
    """
    Validates a URL to prevent Server-Side Request Forgery (SSRF).
    Checks scheme, host, and resolves the host to ensure it points to a public IP.
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False, "Invalid URL scheme. Only HTTP and HTTPS are allowed."

        hostname = parsed.hostname
        if not hostname:
            return False, "Invalid URL format."

        # Resolve hostname to IPs
        try:
            # getaddrinfo returns a list of tuples: (family, type, proto, canonname, sockaddr)
            # sockaddr is a tuple (address, port) for IPv4 or (address, port, flowinfo, scopeid) for IPv6
            addrinfo = socket.getaddrinfo(hostname, parsed.port or 80, proto=socket.IPPROTO_TCP)
        except socket.gaierror:
            return False, f"Could not resolve hostname: {hostname}"

        for info in addrinfo:
            ip = info[4][0]
            if not is_safe_ip(ip):
                return False, f"Unsafe IP address detected: {ip}"

        return True, None
    except Exception as e:
        return False, f"URL validation failed: {str(e)}"

def safe_request(method, url, timeout=10, max_redirects=5, **kwargs):
    """
    Makes a safe HTTP request, protecting against SSRF and redirect loops.
    """
    session = requests.Session()
    session.max_redirects = max_redirects
    current_url = url
    redirects_followed = 0

    while redirects_followed <= max_redirects:
        is_valid, error_msg = validate_url(current_url)
        if not is_valid:
            raise ValueError(f"SSRF Validation Failed: {error_msg}")

        response = session.request(method, current_url, timeout=timeout, allow_redirects=False, **kwargs)

        if response.is_redirect:
            redirect_url = response.headers.get('Location')
            if not redirect_url:
                return response
            # Handle relative redirects
            current_url = urljoin(current_url, redirect_url)
            redirects_followed += 1
        else:
            return response

    raise requests.exceptions.TooManyRedirects(f"Exceeded {max_redirects} redirects.")

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
    except ValueError as e:
        end_time = time.time()
        response_time = end_time - start_time
        return 0, response_time, str(e)
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
        is_valid, error_msg = validate_url(url)
        if not is_valid:
            return None, f"SSRF Validation Failed: {error_msg}"

        hostname = urlparse(url).hostname
        port = urlparse(url).port or 443

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
