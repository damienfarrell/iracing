from sshtunnel import SSHTunnelForwarder
import pymysql
from pymysql.cursors import DictCursor
from config import SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PEM_FILE, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, DATABASE_PASSWORD, DATABASE_DB

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
