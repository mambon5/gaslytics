# Access_token.py

import requests

# Credentials (store safely, ideally outside version control)
EMAIL = "maarja.raap@bkw.ch"
PASSWORD = "Successisontheway2025!"
LOGIN_URL = "https://api.kpler.com/v1/login"


def get_token() -> str:
    """Authenticate with Kpler and return a token using stored credentials."""
    credentials = {"email": EMAIL, "password": PASSWORD}
    response = requests.post(LOGIN_URL, json=credentials)

    if response.status_code != 200:
        raise Exception(f"Login failed: {response.status_code} - {response.text}")

    return response.json().get("token")
