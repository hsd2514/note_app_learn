import sqlite3
from datetime import datetime, timedelta

import pytest

from auth import create_session, delete_session, get_session


@pytest.fixture
def temp_db(tmp_path):
    path = tmp_path / "sessions.db"
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expires_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

    yield str(path)


def test_session_lifecycle(temp_db, monkeypatch):
    """Sessions can be created, read, deleted, and invalid IDs return None."""

    # direct dependency to ensure our helpers hit the temp db
    monkeypatch.setattr("auth.get_connection", lambda db_path: sqlite3.connect(db_path))
    monkeypatch.setattr("auth.close_connection", lambda conn: conn.close())

    session_id = create_session(1, temp_db)
    session = get_session(session_id, temp_db)
    assert session is not None
    assert session["user_id"] == 1
    expires_at = datetime.fromisoformat(session["expires_at"])
    assert expires_at > datetime.now()

    delete_session(session_id, temp_db)
    assert get_session(session_id, temp_db) is None
    assert get_session("does-not-exist", temp_db) is None

