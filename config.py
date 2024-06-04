import os
from dotenv import load_dotenv

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

# iRacing API settings
AUTH_URL = "https://members-ng.iracing.com/auth"
SUBSESSION_URL = "https://members-ng.iracing.com/data/results/get?subsession_id="
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

# Validate environment variables
if not EMAIL or not PASSWORD:
    raise ValueError("EMAIL and PASSWORD environment variables must be set.")
