# verify_db_connection.py
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

try:
    # Attempt to connect to the PostgreSQL database
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("Connection successful!")
    connection.close()
except psycopg2.OperationalError as e:
    print(f"Connection failed: {e}")