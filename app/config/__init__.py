
import os


class Config:
    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    # Keycloak Config
    KEYCLOAK_URL = os.environ.get('KEYCLOAK_URL')
    KEYCLOAK_REALM = os.environ.get('KEYCLOAK_REALM')
    KEYCLOAK_CLIENT_ID = os.environ.get('KEYCLOAK_CLIENT_ID')
    KEYCLOAK_CLIENT_SECRET = os.environ.get('KEYCLOAK_CLIENT_SECRET')
