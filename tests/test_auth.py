import pytest

from auth import hash_password, verify_password


def test_password_hashing_and_verification():
    """Passwords should hash differently from plain text and verify correctly."""
    password = "correct horse battery staple"

    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password

    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)

