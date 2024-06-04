import hashlib
import base64
import requests
import logging
from config import AUTH_URL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def encode_password(email, password):
    """Encode the password using SHA-256 and base64."""
    combined = (password + email.lower()).encode('utf-8')
    initial_hash = hashlib.sha256(combined).digest()
    return base64.b64encode(initial_hash).decode('utf-8')

def authenticate(email, encoded_pw):
    """Authenticate the user and return auth token and cookie."""
    auth_payload = {"email": email, "password": encoded_pw}
    response = requests.post(AUTH_URL, json=auth_payload)
    response.raise_for_status()
    auth_info = response.json()
    sso_cookie_value = auth_info.get("ssoCookieValue")
    auth_token = auth_info.get("authcode")
    if not sso_cookie_value or not auth_token:
        raise ValueError("Authentication failed. No cookie value received.")
    return sso_cookie_value, auth_token

def fetch_session_data(session, url):
    """Fetch data from the given URL."""
    response = session.get(url)
    response.raise_for_status()
    response_link = response.json().get("link")
    if not response_link:
        raise ValueError("Failed to retrieve the data link.")
    data_response = session.get(response_link)
    data_response.raise_for_status()
    return data_response.json()
