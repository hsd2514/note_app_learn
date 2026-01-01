from fastapi import FastAPI
from main import app


def test_app_starts():
    """Verify the FastAPI app object exists and is routable."""
    assert isinstance(app, FastAPI)
    assert hasattr(app, "router")
    assert app.router is not None

