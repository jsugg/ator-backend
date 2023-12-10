from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required
from app.utils.logger import api_logger
from .test_management import test_management_routes
from .performance_testing import performance_testing_routes


api_blueprint: Blueprint = Blueprint('api', __name__)
api_blueprint.register_blueprint(test_management_routes, subdomain='api', url_prefix='/api')
api_blueprint.register_blueprint(performance_testing_routes, subdomain='api', url_prefix='/api')

@api_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected() -> Response:
    """
    A function that handles requests to the '/protected' endpoint.
    
    This function is decorated with the '@api_blueprint.route('/protected', methods=['GET'])'
    decorator, which specifies that the function should handle GET requests to the '/protected'
    endpoint. Additionally, it is decorated with the '@jwt_required()' decorator, which ensures
    that the user must provide a valid JWT in order to access this route.
    
    Parameters:
    None
    
    Returns:
    - A Flask Response object with a JSON payload containing the message "JWT is working!" and a
      status code of 200 if the request is successful.
    - A Flask Response object with a JSON payload containing the error message "Internal server
      error" and a status code of 500 if an exception occurs.
    """
    try:
        api_logger.info("Accessed protected route")
        return jsonify(message="JWT is working!"), 200
    except Exception as e:
        api_logger.error(f"Error in protected route: {str(e)}")
        return jsonify(error="Internal server error"), 500


@api_blueprint.route('/protected', methods=['POST', 'PUT', 'DELETE', 'PATCH'])
@jwt_required()
def protected_methods() -> Response:
    """
    A function that handles requests to the '/protected' route using the methods POST, PUT, DELETE, and PATCH.

    Parameters:
    - None

    Returns:
    - A Response object containing the appropriate response for the request.

    Raises:
    - Any exception that occurs during the execution of the function.

    Side Effects:
    - Logs an info message if there is an attempted access to the protected route with an unsupported method.
    - Logs an error message if there is an error in the protected methods route.

    Error Responses:
    - If the request method is not allowed, returns a JSON response with the error message "Method Not Allowed" and status code 405.
    - If there is an internal server error, returns a JSON response with the error message "Internal server error" and status code 500.
    """
    try:
        api_logger.info("Attempted access to protected route with unsupported method")
        return jsonify(error="Method Not Allowed"), 405
    except Exception as e:
        api_logger.error(f"Error in protected methods route: {str(e)}")
        return jsonify(error="Internal server error"), 500
