"""
Authentication module initialization.
Defines routes, request parsing, and business logic for each resource.
"""
from flask import Blueprint
from . import routes

# Create a Blueprint for the authentication module
auth_blueprint = Blueprint('auth', __name__)

auth_blueprint.register_blueprint(routes.auth_blueprint, subdomain='auth', url_prefix='/auth')
