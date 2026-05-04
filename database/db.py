import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

# Path to the SQLite database file (located in the project root)
_DB_PATH = Path(__file__).resolve().parents[1] / "spendly.db"


def get_db():
    """Return a SQLite connection with row_factory and foreign‑key enforcement.

    The connection points to ``spendly.db`` in the project root.
    """
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create the ``users`` and ``expenses`` tables if they do not exist.
    Safe to call multiple times.
    """
    conn = get_db()
    cursor = conn.cursor()
    # Users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    # Expenses table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    """Insert a demo user and eight sample expenses if the database is empty.
    The function is idempotent – running it again will not duplicate data.
    """
    conn = get_db()
    cursor = conn.cursor()
    # Check whether any user already exists
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Insert demo user
    password_hash = generate_password_hash("demo123")
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    # Sample expenses – one per required category
    expenses = [
        (user_id, 12.5, "Food", "2026-05-01", "Lunch"),
        (user_id, 30.0, "Transport", "2026-05-02", "Taxi"),
        (user_id, 75.0, "Bills", "2026-05-03", "Electricity"),
        (user_id, 20.0, "Health", "2026-05-04", "Pharmacy"),
        (user_id, 45.0, "Entertainment", "2026-05-05", "Movies"),
        (user_id, 100.0, "Shopping", "2026-05-06", "Clothes"),
        (user_id, 60.0, "Other", "2026-05-07", "Gift"),
        (user_id, 15.0, "Food", "2026-05-08", "Coffee"),
    ]
    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    conn.commit()
    conn.close()
