"""Data model definitions for users, sessions, and notes."""

import re
from sqlite3 import Connection


# TODO: Define the raw SQL strings for:
#  - users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT NOT NULL)
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT NOT NULL
);
"""


#  - sessions(id TEXT PRIMARY KEY, user_id INTEGER REFERENCES users(id), expires_at TEXT)
create_sessions_table = """
CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, user_id INTEGER REFERENCES users(id), expires_at TEXT)
"""

#  - notes(id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES users(id), content TEXT, created_at TEXT)
create_notes_table = """
CREATE TABLE IF NOT EXISTS notes(id TEXT PRIMARY KEY, user_id INTEGER REFERENCES users(id), expires_at TEXT)
"""

def init_schema(conn: Connection) -> None:
    """TODO: Run the schema creation statements when the app boots."""
    cursor = conn.cursor()
    cursor.execute(create_notes_table)
    cursor.execute(create_sessions_table)
    cursor.execute(create_users_table)
    conn.commit()
    return True


