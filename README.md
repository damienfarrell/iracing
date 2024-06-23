# iRacing Data Importer

The iRacing Data Importer is a Python API application designed to import race data from the iRacing platform into a MySQL database.

## Features

- Fetch session data based on session ID from the iRacing API.
- Import race results into a MySQL database.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- MySQL Server
- Required Python libraries (install using `pip install -r requirements.txt`)

## Setup

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/damienfarrell/iracing.git
    ```

2. Navigate to the project directory:

    ```bash
    cd iracing-data-importer
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the project root directory and add the following variables:

    ```dotenv
    SSH_HOST=your_ssh_host
    SSH_PORT=your_ssh_port
    SSH_USERNAME=your_ssh_username
    SSH_PEM_FILE=your_ssh_pem_file_path
    DATABASE_HOST=your_database_host
    DATABASE_PORT=your_database_port
    DATABASE_USER=your_database_username
    DATABASE_PASSWORD=your_database_password
    DATABASE_DB=your_database_name
    EMAIL=your_iracing_email
    PASSWORD=your_iracing_password
    ```

## Usage

1. Run the main.py API server:

    ```bash
    uvicorn app.main:app
    ```