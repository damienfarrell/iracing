import os
from dotenv import load_dotenv
import pymysql
from sshtunnel import SSHTunnelForwarder
from pymysql.cursors import DictCursor

# Load environment variables from a .env file
load_dotenv()

# SSH connection settings
SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))  # Default SSH port is 22
SSH_USERNAME = os.getenv('SSH_USERNAME')
SSH_PEM_FILE = os.getenv('SSH_PEM_FILE')

# MySQL connection settings
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = int(os.getenv('DATABASE_PORT', 3306))  # Default MySQL port is 3306
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_DB = os.getenv('DATABASE_DB')

def create_ssh_tunnel():
    """Create an SSH tunnel to the remote MySQL server."""
    return SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USERNAME,
        ssh_pkey=SSH_PEM_FILE,
        remote_bind_address=(DATABASE_HOST, DATABASE_PORT)
    )

def connect_mysql(tunnel):
    """Connect to the MySQL server through the SSH tunnel."""
    try:
        conn = pymysql.connect(
            host=DATABASE_HOST,
            port=tunnel.local_bind_port,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_DB,
            cursorclass=DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Connected to MySQL Server version {version['VERSION()']}")
        return conn
    except pymysql.MySQLError as e:
        print(f"Connection failed: {e}")
        return None

def main():
    """Main function to set up the SSH tunnel and connect to MySQL."""
    with create_ssh_tunnel() as tunnel:
        tunnel.start()
        print(f"SSH tunnel established. Local bind port: {tunnel.local_bind_port}")
        conn = connect_mysql(tunnel)
        if conn:
            # Perform database operations here
            conn.close()
            print("MySQL connection closed.")
        tunnel.stop()

if __name__ == "__main__":
    main()