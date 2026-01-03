import sqlite3

import pytest
from fastapi import FastAPI, Depends, status
from fastapi.testclient import TestClient

import auth
import deps


@pytest.fixture
def temp_db(tmp_path):
    path = tmp_path / "sessions.db"
    conn = sqlite3.connect(path)
    conn.execute(
        """
        CREATE TABLE sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expires_at TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()
    yield str(path)
    # cleanup handled by tmp_path


@pytest.fixture
def client(monkeypatch):
    app = FastAPI()

    @app.get("/protected")
    def protected(user=Depends(deps.get_current_user)):
        return {"user_id": user["user_id"]}

    return TestClient(app)


def test_missing_cookie_returns_401(client):
    response = client.get("/protected")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_valid_session_allows_access(monkeypatch, temp_db, client):
    monkeypatch.setattr(deps, "DB_PATH", temp_db)
    session_id = auth.create_session(42, temp_db)

    client.cookies.set("session_id", session_id)
    response = client.get("/protected")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user_id"] == 42


def test_invalid_session_returns_401(monkeypatch, temp_db, client):
    monkeypatch.setattr(deps, "DB_PATH", temp_db)
    client.cookies.set("session_id", "does-not-exist")
    response = client.get("/protected")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

