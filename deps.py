"""Dependency overrides and request lifecycle utilities."""

from time import timezone
from fastapi import Depends, FastAPI, HTTPException, Request, status
from datetime import datetime,timedelta,timezone
import auth


DB_PATH = "notes.db"


# TODO: Implement `get_current_user` dependency:
#  - read `session_id` cookie from `request.cookies`
#  - call `auth.get_session(session_id, DB_PATH)`
#  - validate `expires_at` and raise `HTTPException(status_code=401)` when missing/expired
#  - return the session row (or at least `{"user_id": ...}`) for downstream handlers
def get_current_user(request: Request) -> dict:
    # 1. Read session_id from cookies
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    # 2. Fetch session from DB
    session = auth.get_session(session_id, DB_PATH)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session",
        )

    # 3. Validate expiration
    try:
        expires_at = datetime.fromisoformat(session["expires_at"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session expiry",
        )

    # IMPORTANT: normalize to UTC if naive
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired",
        )


    return {
        "user_id": session["user_id"]
    }



