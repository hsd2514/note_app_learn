from binascii import a2b_base64
import sqlite3
from fastapi import Depends, FastAPI, HTTPException, Response, responses

import auth
import deps
import models
import notes
from database import get_connection, close_connection

"""Routes wiring for signup/login/notes."""

app = FastAPI()

DB_PATH = "notes.db"


@app.on_event("startup")
def ensure_schema():
    # TODO: Open a connection via database.get_connection and call models.init_schema to create tables.
    deps.DB_PATH = DB_PATH
    conn = get_connection(DB_PATH)
    models.init_schema(conn)
    close_connection(conn)

    pass


@app.get("/")
def listen():
    return "hello world"


# TODO:
#  - POST /signup: hash password, insert into `users`, return 201 or 409.
@app.post("/signup")
def signup(payload: dict):
    username=payload["username"]
    password=payload["password"]

    conn = get_connection(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO users (username,password_hash) VALUES (?,?)",
            (username,auth.hash_password(password)),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409,detail="Username taken")
    finally:
        close_connection(conn)
    return Response(status_code=201)




#  - POST /login: verify credentials, create session, set `session_id` cookie, return 200.
@app.post("/login")
def login(payload: dict):
    username = payload["username"]
    password = payload["password"]

    conn = get_connection(DB_PATH)
    try:
        cursor = conn.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        user_row = cursor.fetchone()
        if not user_row or not auth.verify_password(password, user_row["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        session_id = auth.create_session(user_row["id"], DB_PATH)
        conn.commit()
        # TODO: wrap this in sqlite3.OperationalError handling and return 503 when the auth DB is offline.
    except sqlite3.OperationalError:
        raise HTTPException(status_code=503, detail="Authentication backend unavailable")
    finally:
        close_connection(conn)

    response = Response(status_code=200)
    response.set_cookie("session_id", session_id, httponly=True, samesite="lax")
    return response

#  - POST /notes: protected by deps.get_current_user, call notes.create_note, return 201.
@app.post("/notes")
def create_note(payload: dict, user=Depends(deps.get_current_user)):
    # TODO: catch sqlite3.OperationalError around the notes insert and return 503 with a friendly detail message.
    try:
        notes.create_note(user["user_id"], payload["content"], DB_PATH)
    except sqlite3.OperationalError:
        raise HTTPException(status_code=503, detail="Note storage unavailable")
    return Response(status_code=201)
#  - GET /notes: protected by deps.get_current_user, call notes.list_notes, return the list.
@app.get("/notes")
def list_notes(user=Depends(deps.get_current_user)):
    return [dict(row) for row in notes.list_notes(user["user_id"], DB_PATH)]

