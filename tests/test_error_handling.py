import sqlite3

import pytest
from fastapi.testclient import TestClient

import auth
import deps
import main
import models
import notes


@pytest.fixture
def client(tmp_path):
    main.DB_PATH = str(tmp_path / "errors.db")
    deps.DB_PATH = main.DB_PATH
    conn = sqlite3.connect(main.DB_PATH)
    models.init_schema(conn)
    conn.close()

    with TestClient(main.app) as client:
        yield client


def signup_and_login(client):
    client.post("/signup", json={"username": "alice", "password": "pw"})
    return client.post("/login", json={"username": "alice", "password": "pw"})


def test_note_db_failure_returns_503(client, monkeypatch):
    login_resp = signup_and_login(client)
    assert login_resp.status_code == 200

    def boom_create(user_id, content, db_path):
        raise sqlite3.OperationalError("boom")

    monkeypatch.setattr(notes, "create_note", boom_create)
    response = client.post("/notes", json={"content": "ok"})
    assert response.status_code == 503
    assert "Note storage unavailable" in response.json()["detail"]


def test_session_db_failure_returns_503(client, monkeypatch):
    login_resp = signup_and_login(client)
    assert login_resp.status_code == 200

    def boom_session(session_id, db_path):
        raise sqlite3.OperationalError("boom")

    monkeypatch.setattr(auth, "get_session", boom_session)
    client.cookies.set("session_id", "fake")
    response = client.get("/notes")
    assert response.status_code == 503
    assert "Authentication backend unavailable" in response.json()["detail"]

