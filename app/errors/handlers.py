from typing import Tuple
from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

error_blueprint = Blueprint('errors', __name__)


def handle_http_exception(error: HTTPException) -> Tuple[jsonify, int]:
    """
    Generic handler for HTTP exceptions.

    Args:
        error (HTTPException): The HTTP exception that occurred.

    Returns:
        Tuple[jsonify, int]: A JSON response with error details and the HTTP status code.
    """
    response = jsonify({'error': error.description})
    response.status_code = error.code
    return response


@error_blueprint.errorhandler(Exception)
def handle_exception(error: Exception) -> Tuple[jsonify, int]:
    """
    Generic handler for all other exceptions.

    Args:
        error (Exception): The exception that occurred.

    Returns:
        Tuple[jsonify, int]: A JSON response with error details and a 500 status code.
    """
    return jsonify({'error': str(error)}), 500


@error_blueprint.app_errorhandler(400)
@error_blueprint.app_errorhandler(401)
@error_blueprint.app_errorhandler(403)
@error_blueprint.app_errorhandler(404)
@error_blueprint.app_errorhandler(405)
@error_blueprint.app_errorhandler(500)
def error_handler(error: HTTPException) -> Tuple[jsonify, int]:
    """
    Specific handler for HTTP errors.

    Args:
        error (HTTPException): The HTTP exception corresponding to the error code.

    Returns:
        Tuple[jsonify, int]: A JSON response with error details and the corresponding status code.
    """
    return handle_http_exception(error)
