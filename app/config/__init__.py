
import os


class Config:
    # General Config
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'secret_key'
    # Keycloak Config
    KEYCLOAK_URL: str = os.environ.get('KEYCLOAK_URL')
    KEYCLOAK_REALM: str = os.environ.get('KEYCLOAK_REALM')
    KEYCLOAK_CLIENT_ID: str = os.environ.get('KEYCLOAK_CLIENT_ID')
    KEYCLOAK_CLIENT_SECRET: str = os.environ.get('KEYCLOAK_CLIENT_SECRET')
