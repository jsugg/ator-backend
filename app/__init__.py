from flask import Flask
from .config import config_by_name
from .extensions import init_app, db, migrate, jwt, oauth
from .api import api_blueprint
from .auth import auth_blueprint
from .errors.handlers import error_blueprint

def create_app(config_name: str) -> Flask:
    """
    Create and configure an instance of the Flask application.

    Args:
        config_name (str): The configuration name to use (e.g., 'development', 'testing', 'production').

    Returns:
        Flask: The configured Flask application.
    """
    app: Flask = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    init_app(app)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(error_blueprint)

    return app
