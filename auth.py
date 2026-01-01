"""Authentication helpers and password/session logic."""

import bcrypt


# TODO: Sessions store server-side session IDs and reference `users.id`.
# Implement bcrypt-based `hash_password` and `verify_password` helpers.


def hash_password(plain: str) -> str:
    """Return a bcrypt hash for the clear-text password."""
    hashed = bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Check that a plain password matches the stored bcrypt hash."""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

