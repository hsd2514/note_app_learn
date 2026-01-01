from ast import If, main
from os import name
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def listen():
    return "hello world"

# TODO: Add route handlers (signup/login, notes endpoints) once the dependencies are implemented.


