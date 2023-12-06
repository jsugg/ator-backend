from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required
from .test_management import test_management_routes
from .performance_testing import performance_testing_routes

api_blueprint: Blueprint = Blueprint('api', __name__)
api_blueprint.register_blueprint(test_management_routes)
api_blueprint.register_blueprint(performance_testing_routes)

@api_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected() -> Response:
    return jsonify(message="JWT is working!"), 200


@api_blueprint.route('/protected', methods=['POST', 'PUT', 'DELETE', 'PATCH'])
@jwt_required()
def protected_methods() -> Response:
    return jsonify(error="Method Not Allowed"), 405
