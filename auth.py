"""Authentication helpers and password/session logic."""

import secrets
import datetime
from time import timezone
import bcrypt
from database import get_connection,close_connection
import sqlite3
from datetime import datetime, timezone , timedelta



# TODO: Sessions store server-side session IDs and reference `users.id`.
# TODO: Implement bcrypt-based `hash_password`/`verify_password` helpers.
# TODO: Add `create_session(user_id: int) -> str` that inserts into `sessions`.
# TODO: Add `get_session(session_id: str)` to read session metadata from the DB.
# TODO: Add `delete_session(session_id: str)` for logout and cleanup.


def hash_password(plain: str) -> str:
    """Return a bcrypt hash for the clear-text password."""
    hashed = bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Check that a plain password matches the stored bcrypt hash."""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_session(user_id: int, db_path: str) -> str:
    session_id = secrets.token_urlsafe()

    expiry = (
        datetime.now(timezone.utc)
        .replace(tzinfo=None)   
        + timedelta(days=1)
    ).isoformat()

    conn = get_connection(db_path)
    conn.execute(
        "INSERT INTO sessions (id,user_id,expires_at) VALUES (?,?,?)",
        (session_id, user_id, expiry)
    )
    conn.commit()
    close_connection(conn)

    return session_id

    




    



def get_session(session_id: str, db_path: str):
    """Query the `sessions` table to fetch session info (user_id, expiry, etc.)."""
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    user = conn.execute(
        "SELECT * FROM sessions WHERE id = ?",
        (session_id,)
    ).fetchone()
    close_connection(conn)
    return user




    




def delete_session(session_id: str, db_path: str) -> None:
    conn = get_connection(db_path)

    conn.execute(
        "DELETE FROM sessions WHERE id = ?",
        (session_id,)
    )
    conn.commit()        
    close_connection(conn)
