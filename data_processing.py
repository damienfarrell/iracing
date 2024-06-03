import hashlib
import base64
import requests
import logging
import pymysql
from config import AUTH_URL, EMAIL, PASSWORD, DATA_URL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def encode_pw(EMAIL, PASSWORD):
    """Encode the password using SHA-256 and base64."""
    combined = (PASSWORD + EMAIL.lower()).encode('utf-8')
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

def fetch_data(session, DATA_URL):
    """Fetch data from the given URL."""
    response = session.get(DATA_URL)
    response.raise_for_status()
    response_link = response.json().get("link")
    if not response_link:
        raise ValueError("Failed to retrieve the data link.")
    data_response = session.get(response_link)
    data_response.raise_for_status()
    data = data_response.json()
    return data

def test_db(conn):
    query = "SELECT * FROM wp_iracing_results_teams"
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print(row)
            return results
    except pymysql.MySQLError as e:
        print(f"An error occurred: {e}")
        return None


def import_to_db(conn, data):

    query = """
    INSERT INTO wp_iracing_results_teams (
    fin_pos, car_id, Car, car_class_id, car_class, team_id, cust_id, Name, start_pos, car_number, out_id, `Out`, `Interval`, laps_led, qualify_time, average_lap_time, fastest_lap_time, fastest_lap_number, laps_comp, Inc, club_id, Club, max_pct_fuel_fill, weight_penalty_kg, session_name, AI, race, `group`
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    with conn.cursor() as cursor:
        for result in data["session_results"][0]["results"]:
            cursor.execute(query, (
                result["finish_position"],
                result["car_id"],
                result["car_name"],
                result["car_class_id"],
                result["car_class_name"],
                result["cust_id"],
                result["cust_id"],
                result["display_name"],
                result["starting_position"],
                result["livery"]["car_number"],
                result["reason_out_id"],
                result["reason_out"],
                result["interval"],
                result["laps_lead"],
                result["best_qual_lap_at"],
                result["average_lap"],
                result["best_lap_time"],
                result["best_lap_num"],
                result["laps_complete"],
                result["incidents"],
                result["club_id"],
                result["club_name"],
                result["max_pct_fuel_fill"],
                result["weight_penalty_kg"],
                data.get("session_name"),
                result["ai"],
                1,
                6
            ))
        conn.commit()
    logging.info("Data imported into the database successfully.")