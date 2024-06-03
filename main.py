import hashlib
import base64
from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd
from pathlib import Path
import logging

# Load environment variables
load_dotenv()

# Configuration and Constants
ROOT_URL = "https://members-ng.iracing.com/data/results/get?subsession_id="
AUTH_URL = "https://members-ng.iracing.com/auth"
SESSION_ID = 67471739
DATA_URL = f"{ROOT_URL}{SESSION_ID}"
CSV_FILE_PATH = Path("data.csv")
JSON_FILE_PATH = Path("data.json")
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

# Variables
race_number = 1
group_number = 6

# Validate environment variables
if not EMAIL or not PASSWORD:
    raise ValueError("EMAIL and PASSWORD environment variables must be set.")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def encode_pw(email, password):
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

def fetch_data(session, data_url):
    """Fetch data from the given URL."""
    response = session.get(data_url)
    response.raise_for_status()
    response_link = response.json().get("link")
    if not response_link:
        raise ValueError("Failed to retrieve the data link.")
    data_response = session.get(response_link)
    data_response.raise_for_status()
    return data_response.json()

def save_json(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def process_data(json_file_path, csv_file_path):
    """Process JSON data and save it to a CSV file."""
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    results = []
    for result in data["session_results"][0]["results"]:
        results.append({
            "Fin Pos": result["finish_position"],
            "Car ID": result["car_id"],
            "Car": result["car_name"],
            "Car Class ID": result["car_class_id"],
            "Car Class": result["car_class_name"],
            "Team ID": result["cust_id"],
            "Cust ID": result["cust_id"],
            "Name": result["display_name"],
            "Start Pos": result["starting_position"],
            "Car #": result["livery"]["car_number"],
            "Out ID": result["reason_out_id"],
            "Out": result["reason_out"],
            "Interval": result["interval"],
            "Laps Led": result["laps_lead"],
            "Qualify Time": result["best_qual_lap_at"],
            "Average Lap Time": result["average_lap"],
            "Fastest Lap Time": result["best_lap_time"],
            "Fast Lap#": result["best_lap_num"],
            "Laps Comp": result["laps_complete"],
            "Inc": result["incidents"],
            "Club ID": result["club_id"],
            "Club": result["club_name"],
            "Max Fuel Fill%": result["max_pct_fuel_fill"],
            "Weight Penalty (KG)": result["weight_penalty_kg"],
            "Session Name": data.get("session_name"),
            "AI": result["ai"],
            "race": race_number,
            "group": group_number  
        })

    df = pd.DataFrame(results)
    df.to_csv(csv_file_path, index=False)
    logging.info(f"Data has been exported to {csv_file_path}")
    print(df)

def main():
    try:
        pw_value_to_submit = encode_pw(EMAIL, PASSWORD)
        
        sso_cookie_value, auth_token = authenticate(EMAIL, pw_value_to_submit)
        
        session = requests.Session()
        session.cookies.update({
            "irsso_membersv2": sso_cookie_value,
            "authtoken_members": f'{{"authtoken":{{"authcode":"{auth_token}","email":"{EMAIL}"}}}}'
        })
        
        data = fetch_data(session, DATA_URL)
        save_json(data, JSON_FILE_PATH)
        logging.info(f"Data successfully exported to {JSON_FILE_PATH}")
        
        process_data(JSON_FILE_PATH, CSV_FILE_PATH)

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred during the request: {e}")
    except ValueError as e:
        logging.error(f"An error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()