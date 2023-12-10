from flask import Flask
from .config import config_by_name
from .extensions import init_app
from .api import api_blueprint
from .auth import auth_blueprint
from .errors.handlers import error_blueprint
from .utils.logger import app_logger

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

    try:
        app.register_blueprint(api_blueprint, url_prefix='/api')
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(error_blueprint)
        init_app(app)
        app_logger.info(f"App created with {config_name} configuration.")
    except Exception as err:
        app_logger.error(f"Error in creating app: {str(err)}")
    
    return app
