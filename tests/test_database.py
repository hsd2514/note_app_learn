import sqlite3

import pytest

from database import close_connection, get_connection


def test_database_connection_lifecycle(tmp_path):
    """Ensure get_connection opens a row-accessible connection and close_connection tears it down."""
    db_path = tmp_path / "exercise2.db"

    conn = get_connection(str(db_path))
    assert isinstance(conn, sqlite3.Connection)
    assert conn.row_factory == sqlite3.Row

    close_connection(conn)
    with pytest.raises(sqlite3.ProgrammingError):
        conn.execute("SELECT 1")

