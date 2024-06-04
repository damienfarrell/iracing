import logging
import requests
from import_data import import_race_data
from get_data import encode_password, authenticate, fetch_session_data
from config import EMAIL, PASSWORD, SUBSESSION_URL
from menu import display_menu, get_session_parameters

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        pw_value_to_submit = encode_password(EMAIL, PASSWORD)
        sso_cookie_value, auth_token = authenticate(EMAIL, pw_value_to_submit)
        session = requests.Session()
        session.cookies.update({
            "irsso_membersv2": sso_cookie_value,
            "authtoken_members": f'{{"authtoken":{{"authcode":"{auth_token}","email":"{EMAIL}"}}}}'
        })
        
        choice = display_menu()
        if choice == "1":
            session_url, race, group = get_session_parameters(SUBSESSION_URL)
            logging.info(f"Session URL:{session_url} Race: {race} Group {group}")
            data = fetch_session_data(session, session_url)
            import_race_data(data, race, group)
        elif choice == "2":
            print("TBC option selected.")
        else:
            print("Invalid choice.")

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred during the request: {e}")
    except ValueError as e:
        logging.error(f"An error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
