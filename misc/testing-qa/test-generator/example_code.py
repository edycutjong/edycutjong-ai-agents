def calculate_area(length, width):
    """Calculates the area of a rectangle."""
    if length < 0 or width < 0:
        raise ValueError("Length and width must be non-negative.")
    return length * width

def is_palindrome(s):
    """Checks if a string is a palindrome."""
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

import requests

def fetch_user_data(user_id):
    """Fetches user data from an external API."""
    if not user_id:
        raise ValueError("User ID cannot be empty.")

    response = requests.get(f"https://api.example.com/users/{user_id}")
    if response.status_code != 200:
        return None

    return response.json()
