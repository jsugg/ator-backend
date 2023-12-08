import os
from typing import Dict, Type

class Config:
    """
    Base configuration class with common settings.

    Attributes:
        SECRET_KEY (str): Secret key for the application.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to track modifications in SQLAlchemy.
        KEYCLOAK_URL (str): URL of the Keycloak server.
        KEYCLOAK_REALM (str): Keycloak realm name.
        KEYCLOAK_CLIENT_ID (str): Keycloak client ID.
        KEYCLOAK_CLIENT_SECRET (str): Keycloak client secret.
        JWT_SECRET_KEY (str): Secret key for JWT.
    """
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'secret')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    KEYCLOAK_URL: str = os.getenv('KEYCLOAK_URL')
    KEYCLOAK_REALM: str = os.getenv('KEYCLOAK_REALM')
    KEYCLOAK_CLIENT_ID: str = os.getenv('KEYCLOAK_CLIENT_ID')
    KEYCLOAK_CLIENT_SECRET: str = os.getenv('KEYCLOAK_CLIENT_SECRET')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'jwt_secret')
    CELERY_BROKER_URL: str = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND: str = os.getenv('CELERY_RESULT_BACKEND')
    SWAGGER_URL: str = os.getenv('SWAGGER_URL')
    SWAGGERAPI_URL: str = os.getenv('SWAGGER_API_URL')


class DevelopmentConfig(Config):
    """
    Development specific configuration.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): Database URI for development environment.
        DEBUG (bool): Debug mode flag.
    """
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DEV_DATABASE_URI', 'sqlite:///dev.db')
    DEBUG: bool = True

class TestingConfig(Config):
    """
    Testing specific configuration.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): Database URI for testing environment.
        TESTING (bool): Testing mode flag.
    """
    SQLALCHEMY_DATABASE_URI: str = os.getenv('TEST_DATABASE_URI', 'sqlite:///test.db')
    TESTING: bool = True

class ProductionConfig(Config):
    """
    Production specific configuration.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): Database URI for production environment.
        DEBUG (bool): Debug mode flag.
    """
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URI', 'sqlite:///prod.db')
    DEBUG: bool = False

config_by_name: Dict[str, Type[Config]] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
