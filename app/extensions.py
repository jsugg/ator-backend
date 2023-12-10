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
keycloak: OAuth = OAuth()

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
    try:
        influxdb = InfluxDBClient(
            host='influxdb_host', port=8086, username='admin', password='admin'
        )
        return influxdb

    except Exception as err:
        app_logger.error(f"Error in creating InfluxDB client: {str(err)}")
        raise err


influxdb_client: InfluxDBClient = create_influxdb_client()


def create_redis_client() -> Redis:
    """
    Create and return a Redis client.

    Returns:
        Redis: An instance of Redis client.
    """
    try:
        redis: Redis = Redis(
            host='redis_host', port=6379, db=0, decode_responses=True
        )
        return redis

    except Exception as err:
        app_logger.error(f"Error in creating Redis client: {str(err)}")
        raise err


redis_client: Redis = create_redis_client()


def create_keycloak_oauth(app: Flask) -> OAuth:
    """
    Configure and return Keycloak OAuth client.

    Args:
        app (Flask): The Flask application instance to be configured.

    Returns:
        OAuth: Configured OAuth client for Keycloak.
    """
    try:
        keycloak: OAuth = OAuth(app)
        # app_logger.info(f"'kc_cid': {app.config['KEYCLOAK_CLIENT_ID']}, 'kc_secret': {app.config['KEYCLOAK_CLIENT_SECRET']}, 'kc_url': {app.config['KEYCLOAK_URL']}, 'kc_realm': {app.config['KEYCLOAK_REALM']}")
        keycloak.remote_app(
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

    except Exception as err:
        app_logger.error(f"Error in creating Keycloak OAuth: {str(err)}")
        raise err


def create_celery(app: Flask) -> Celery:
    """
    Create and return a Celery instance.

    Args:
        app (Flask): The Flask application instance to be used.

    Returns:
        Celery: A Celery instance.
    """
    try:
        celery = Celery(
            app.import_name,
            backend=app.config['CELERY_RESULT_BACKEND'],
            broker=app.config['CELERY_BROKER_URL']
        )

        celery.conf.update(app.config)
        return celery

    except Exception as err:
        app_logger.error(f"Error in creating Celery: {str(err)}")
        raise err


def create_swagger(app: Flask) -> Api:
    """
    Create and return a Swagger API instance.

    Args:
        app (Flask): The Flask application instance to be used.

    Returns:
        Api: A Swagger API instance.
    """
    try:
        SWAGGER_URL: str = app.config['SWAGGER_URL']
        SWAGGER_API_URL: str = app.config['SWAGGER_API_URL']
        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL, SWAGGER_API_URL)
        app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
        swagger_api = Api(app, title='API', version='1.0',
                          description='API documentation using Swagger', doc=SWAGGER_URL)
        app_logger.info("Swagger created successfully.")

    except Exception as err:
        app_logger.error(f"Error in creating Swagger: {str(err)}")
        raise err
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
        with app.app_context():
            db.create_all()
        migrate.init_app(app, db)
        jwt.init_app(app)
        create_keycloak_oauth(app)
        create_swagger(app)
        app_logger.info("Flask extensions initialized successfully.")
    except Exception as err:
        app_logger.error(f"Error in initializing Flask extensions: {str(err)}")
        raise err
