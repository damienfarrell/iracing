import hashlib
import base64
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

ROOT_URL = "https://members-ng.iracing.com/data/results/get?subsession_id="
session_id = 67471739
AUTH_URL = "https://members-ng.iracing.com/auth"
DATA_URL = ROOT_URL + str(session_id)

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

# Check if email and password are set
if not EMAIL or not PASSWORD:
    raise ValueError("EMAIL and PASSWORD environment variables must be set.")

def encode_pw(email, password):
    combined = (password + email.lower()).encode('utf-8')
    initial_hash = hashlib.sha256(combined).digest()
    hash_in_base64 = base64.b64encode(initial_hash).decode('utf-8')
    return hash_in_base64

# Encode the password
pw_value_to_submit = encode_pw(EMAIL, PASSWORD)

# Prepare authentication payload
auth_dict = {
    "email": EMAIL,
    "password": pw_value_to_submit
}

try:
    # Authenticate and get auth token and cookie
    response = requests.post(AUTH_URL, json=auth_dict)
    response.raise_for_status()
    
    auth_info = response.json()
    
    sso_cookie_value = auth_info.get("ssoCookieValue")
    auth_token = auth_info.get("authcode")
    
    if not sso_cookie_value or not auth_token:
        raise ValueError("Authentication failed. No cookie value received.")

    # Start session and set cookies
    session = requests.Session()
    cookies = {
        "irsso_membersv2": sso_cookie_value,
        "authtoken_members": f'{{"authtoken":{{"authcode":"{auth_token}","email":"{EMAIL}"}}}}'
    }
    session.cookies.update(cookies)

    # Fetch data URL
    response = session.get(DATA_URL)
    response.raise_for_status()
    
    response_link = response.json().get("link")
    if not response_link:
        raise ValueError("Failed to retrieve the data link.")
    
    # Fetch the actual data
    data_response = session.get(response_link)
    data_response.raise_for_status()
    
    data = data_response.json()

    # Specify the file name
    file_name = 'data.json'
    
    # Write the data to a JSON file
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Data successfully exported to {file_name}")


except requests.exceptions.RequestException as e:
    print(f"An error occurred during the request: {e}")
except ValueError as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")