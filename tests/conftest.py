import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from app.extensions import db as _db
from typing import Generator, Any


@pytest.fixture(scope='session')
def app() -> Flask:
    """
    Pytest fixture for creating a Flask application instance for testing.

    Returns:
        Flask: The Flask application instance.
    """
    app = create_app('testing')
    return app


@pytest.fixture(scope='session')
def db(app: Flask) -> Generator[SQLAlchemy, Any, None]:
    """
    Pytest fixture for setting up and tearing down a database for tests.

    Args:
        app (Flask): The Flask application instance for the context.

    Yields:
        Generator[SQLAlchemy, Any, None]: SQLAlchemy database instance.
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()
