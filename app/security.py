from flask_security import Security, SQLAlchemyUserDatastore
from app.db.models import User, Role
from app.extensions import db
from flask import Flask
from typing import NoReturn

# Type hinting for the SQLAlchemyUserDatastore with User and Role models.
user_datastore: SQLAlchemyUserDatastore[User, Role] = SQLAlchemyUserDatastore(db, User, Role)

# Type hinting for the Security instance.
security: Security = Security()

def init_security(app: Flask) -> NoReturn:
    """
    Initialize security features for the Flask application.

    Args:
        app (Flask): The Flask application instance to be configured.

    This function sets up the user datastore and initializes the Security extension,
    integrating it with the Flask application.
    """
    security.init_app(app, user_datastore)
