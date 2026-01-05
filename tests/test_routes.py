import sqlite3

from fastapi.testclient import TestClient

import deps
import main
import models


def test_routes_flow(tmp_path):
    main.DB_PATH = str(tmp_path / "routes.db")
    deps.DB_PATH = main.DB_PATH

    conn = sqlite3.connect(main.DB_PATH)
    models.init_schema(conn)
    conn.close()

    with TestClient(main.app) as client:
        response = client.post("/signup", json={"username": "alice", "password": "pw"})
        assert response.status_code == 201

        assert client.get("/notes").status_code == 401

        login_resp = client.post("/login", json={"username": "alice", "password": "pw"})
        assert login_resp.status_code == 200
        assert "session_id" in login_resp.cookies

        create_resp = client.post("/notes", json={"content": "hello"})
        assert create_resp.status_code == 201

        read_resp = client.get("/notes")
        assert read_resp.status_code == 200
        notes_list = read_resp.json()
        assert isinstance(notes_list, list)
        assert notes_list and notes_list[0]["content"] == "hello"

