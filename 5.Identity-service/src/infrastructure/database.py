import os
from contextlib import contextmanager

import pyodbc

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_USER = os.getenv("DB_NAME", "OK2SHIP_SMT")
DB_NAME = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "YourStrong(!)Password")

CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}}"
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={DB_HOST},{DB_PORT};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=yes;"  # Bắt buộc phải có để bypass SSL certificate khi chạy container nội bộ
    f"Connection Timeout=30;"
)


@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = pyodbc.connect(CONNECTION_STRING)
        yield connection
    except pyodbc.Error as e:
        print(f"Connection failed: {e}")
    finally:
        if connection:
            connection.close
