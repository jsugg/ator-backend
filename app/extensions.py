from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_oauthlib.client import OAuth
from redis import Redis
from influxdb import InfluxDBClient
from flask import Flask
from typing import NoReturn
from celery import Celery
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restx import Api
from flask_cors import CORS  # TODO
from .utils.logger import app_logger

# Database ORM
db: SQLAlchemy = SQLAlchemy()

# Database migration tool
migrate: Migrate = Migrate()

# JSON Web Token manager
jwt: JWTManager = JWTManager()

# OAuth client
oauth: OAuth = OAuth()

# Celery
celery: Celery = Celery()

# Swagger API
swagger_api: Api = Api()

def create_influxdb_client() -> InfluxDBClient:
    """
    Create and return an InfluxDB client.

    Returns:
        InfluxDBClient: An instance of InfluxDBClient.
    """
    return InfluxDBClient(
        host='influxdb_host', port=8086, database='performance_data'
    )


influxdb_client: InfluxDBClient = create_influxdb_client()


def create_redis_client() -> Redis:
    """
    Create and return a Redis client.

    Returns:
        Redis: An instance of Redis client.
    """
    return Redis(
        host='redis_host', port=6379, db=0, decode_responses=True
    )


redis_client: Redis = create_redis_client()


def create_keycloak_oauth(app: Flask) -> OAuth:
    """
    Configure and return Keycloak OAuth client.

    Args:
        app (Flask): The Flask application instance to be configured.

    Returns:
        OAuth: Configured OAuth client for Keycloak.
    """
    keycloak_oauth: OAuth = OAuth(app)
    keycloak_oauth.remote_app(
        'keycloak',
        consumer_key=app.config['KEYCLOAK_CLIENT_ID'],
        consumer_secret=app.config['KEYCLOAK_CLIENT_SECRET'],
        request_token_params={'scope': 'openid'},
        base_url=app.config['KEYCLOAK_URL'],
        access_token_url='/realms/' +
        app.config['KEYCLOAK_REALM'] + '/protocol/openid-connect/token',
        authorize_url='/realms/' +
        app.config['KEYCLOAK_REALM'] + '/protocol/openid-connect/auth',
    )
    return keycloak_oauth


def create_celery(app: Flask) -> Celery:
    """
    Create and return a Celery instance.

    Args:
        app (Flask): The Flask application instance to be used.

    Returns:
        Celery: A Celery instance.
    """
    celery: Celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )

    celery.conf.update(app.config)
    return celery


def create_swagger(app: Flask) -> Api:
    SWAGGER_URL: str = app.config['SWAGGER_URL']
    SWAGGER_API_URL: str = app.config['SWAGGER_API_URL']
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, SWAGGER_API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    swagger_api = Api(app, title='API', version='1.0',
                      description='API documentation using Swagger', doc=SWAGGER_URL)
    swagger_api.add_namespace(swaggerui_blueprint, path='/api')
    return swagger_api

def init_app(app: Flask) -> NoReturn:
    """
    Initialize the application with Flask extensions.

    Args:
        app (Flask): The Flask application instance to be initialized.
    """
    try:
        app_logger.info("Initializing Flask extensions...")
        db.init_app(app)
        migrate.init_app(app, db)
        jwt.init_app(app)
        oauth.init_app(app)
        create_swagger(app)
        app_logger.info("Flask extensions initialized successfully.")
    except Exception as err:
        app_logger.error(f"Error in initializing Flask extensions: {str(err)}")
        raise err