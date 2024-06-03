import logging
import requests
from database import create_ssh_tunnel, connect_mysql
from data_processing import encode_pw, authenticate, fetch_data, import_to_db, test_db
from config import EMAIL, PASSWORD, DATA_URL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

        with create_ssh_tunnel() as tunnel:
            tunnel.start()
            print(f"SSH tunnel established. Local bind port: {tunnel.local_bind_port}")
            conn = connect_mysql(tunnel)
            if conn:
                import_to_db(conn, data)
                conn.close()
                print("MySQL connection closed.")
            tunnel.stop()

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred during the request: {e}")
    except ValueError as e:
        logging.error(f"An error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()