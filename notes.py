"""Note-specific business logic."""

from datetime import datetime
from typing import List

import sqlite3

from database import Connection, get_connection, close_connection


# TODO: Implement `create_note(user_id: int, content: str, db_path: str) -> int`.
#  - Use raw SQL to insert a note row in the `notes` table.
#  - Always scope operations by `user_id`.
#  - Return the new note ID.
def create_note(user_id: int,content: str,db_paths:str)->int:
    conn = get_connection(db_paths)
    cursor=conn.execute("INSERT INTO notes (user_id,content,created_at) VALUES (?,?,?)",(user_id,content,datetime.now().isoformat()))
    notes_id = cursor.lastrowid

    conn.commit()
    close_connection(conn)
    return notes_id


# TODO: Implement `list_notes(user_id: int, db_path: str) -> List[sqlite3.Row]`.
#  - Query the `notes` table for the user’s notes only and return row objects.
#  - Keep the per-request connection lifecycle with `get_connection`/`close_connection`.
def list_notes(user_id: int, db_path: str) -> List[sqlite3.Row]:
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
    "SELECT * FROM notes WHERE user_id = ?",
    (user_id,),
).fetchall()


    close_connection(conn)
    return cursor



