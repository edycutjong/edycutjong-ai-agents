import requests
import jwt
import urllib.parse
import re

def generate_auth_url(client_id, auth_url, redirect_uri, scopes, state=None):
    """
    Generates the authorization URL for the Authorization Code flow.
    """
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scopes
    }
    if state:
        params["state"] = state

    # Handle existing query params in auth_url
    url_parts = list(urllib.parse.urlparse(auth_url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)

    return urllib.parse.urlunparse(url_parts)

def exchange_code_for_token(client_id, client_secret, token_url, code, redirect_uri):
    """
    Exchanges an authorization code for an access token.
    """
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }
    try:
        response = requests.post(token_url, data=data)
        # response.raise_for_status() # Let the caller handle checking for errors in the returned dict, or handle it here.
        # It's better to return the full response content even if error, so the debugger can show it.

        try:
            return response.json()
        except ValueError:
            return {"error": "Invalid JSON response", "body": response.text, "status_code": response.status_code}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_client_credentials_token(client_id, client_secret, token_url, scopes):
    """
    Obtains an access token using the Client Credentials flow.
    """
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scopes
    }
    try:
        response = requests.post(token_url, data=data)
        try:
            return response.json()
        except ValueError:
            return {"error": "Invalid JSON response", "body": response.text, "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def refresh_access_token(client_id, client_secret, token_url, refresh_token):
    """
    Refreshes an access token using a refresh token.
    """
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
    try:
        response = requests.post(token_url, data=data)
        try:
            return response.json()
        except ValueError:
             return {"error": "Invalid JSON response", "body": response.text, "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def decode_jwt(token):
    """
    Decodes a JWT token without verification to inspect its contents.
    """
    try:
        # Decode without verification to inspect headers and payload
        header = jwt.get_unverified_header(token)
        payload = jwt.decode(token, options={"verify_signature": False})
        return {"header": header, "payload": payload, "valid_structure": True}
    except jwt.DecodeError as e:
        return {"error": str(e), "valid_structure": False}

def validate_redirect_uri(uri):
    """
    Validates a Redirect URI for common issues.
    """
    issues = []

    if not uri:
         return ["URI is empty"]

    try:
        parsed = urllib.parse.urlparse(uri)
    except Exception:
        return ["Invalid URL format"]

    if parsed.scheme != "https":
        if parsed.hostname not in ["localhost", "127.0.0.1", "::1"]:
             issues.append("Redirect URI must use HTTPS unless strictly local (localhost/127.0.0.1).")

    if "#" in uri:
        issues.append("Redirect URI must not contain a fragment identifier (#).")

    if not parsed.path or parsed.path == "/":
        # This is a soft warning, some providers might allow root, but usually it's a specific path
        pass

    # Check for query params which are sometimes allowed but often discouraged or handled specifically
    if parsed.query:
        # issues.append("Redirect URI usually should not contain query parameters.")
        pass

    return issues
