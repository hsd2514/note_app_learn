"""Database connection helpers."""

import sqlite3
from sqlite3 import Connection


def get_connection(db_path: str) -> Connection:
    """
    Open a SQLite connection per request (no global connection!) and configure
    `row_factory` so callers can access columns by name.
    """

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def close_connection(conn: Connection) -> None:
    """Close the request-scoped SQLite connection."""
    conn.close()

