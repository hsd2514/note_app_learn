import sqlite3

import pytest

import notes


@pytest.fixture
def temp_db(tmp_path):
    path = tmp_path / "notes.db"
    conn = sqlite3.connect(path)
    conn.execute(
        """
        CREATE TABLE notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
    yield str(path)


def test_user_notes_isolation(temp_db):
    note_id = notes.create_note(1, "first note", temp_db)
    assert isinstance(note_id, int)

    user_notes = notes.list_notes(1, temp_db)
    assert len(user_notes) == 1
    assert user_notes[0]["content"] == "first note"

    other_notes = notes.list_notes(2, temp_db)
    assert other_notes == []




