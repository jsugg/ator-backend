"""
Authentication module initialization.
Defines routes, request parsing, and business logic for each resource.
"""
from flask import Blueprint
from . import routes

# Create a Blueprint for the authentication module
auth = Blueprint('auth', __name__)
