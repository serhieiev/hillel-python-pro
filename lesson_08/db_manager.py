import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    @staticmethod
    def get_connection():
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )

    @staticmethod
    def get_cursor(connection):
        return connection.cursor()
