import sqlite3

import pytest

from models import init_schema


def test_schema_initializes_tables(tmp_path):
    """Ensure the users, sessions, and notes tables exist after initialization."""
    db_path = tmp_path / "schema.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    init_schema(conn)

    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    table_names = {row["name"] for row in cursor}
    assert {"users", "sessions", "notes"}.issubset(table_names)

    conn.close()

