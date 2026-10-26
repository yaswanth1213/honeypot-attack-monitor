
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("honeypot.db")


def initialize_database():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                client_ip TEXT NOT NULL,
                username TEXT NOT NULL,
                event TEXT NOT NULL
            )
        """)


def save_attempt(timestamp, client_ip, username, event):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO login_attempts
            (timestamp, client_ip, username, event)
            VALUES (?, ?, ?, ?)
        """, (timestamp, client_ip, username, event))


def get_attempts():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("""
            SELECT id, timestamp, client_ip, username, event
            FROM login_attempts
            ORDER BY id DESC
        """)
        return cursor.fetchall()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")
    print("Database path:", DB_FILE)
