from typing import Literal
from flask import Blueprint, Response, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.models import TestSuite, TestCase
from app.db import db
from app.services.test_execution_service import execute_test_suite
test_management_routes = Blueprint('test_management', __name__)
from app.api import performance_testing_routes

@test_management_routes.route('/testsuites', methods=['GET', 'POST'])
@jwt_required()
def test_suites():
    if request.method == 'GET':
        return jsonify([suite.to_dict() for suite in TestSuite.query.all()])

    elif request.method == 'POST':
        data = request.get_json()
        new_suite = TestSuite(
            name=data['name'], description=data.get('description', ''))
        db.session.add(new_suite)
        db.session.commit()
        return jsonify(new_suite.to_dict()), 201


@test_management_routes.route('/testsuites/<int:suite_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def test_suite(suite_id):
    suite = TestSuite.query.get_or_404(suite_id)

    if request.method == 'GET':
        return jsonify(suite.to_dict())

    elif request.method == 'PUT':
        data = request.get_json()
        suite.name = data.get('name', suite.name)
        suite.description = data.get('description', suite.description)
        db.session.commit()
        return jsonify(suite.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(suite)
        db.session.commit()
        return jsonify({}), 204


@performance_testing_routes.route('/execute-suite/<int:suite_id>', methods=['POST'])
@jwt_required()
def execute_suite(suite_id):
    try:
        results = execute_test_suite(suite_id)
        return jsonify(results), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@test_management_routes.route('/testsuites/<int:suite_id>/testcases', methods=['POST'])
@jwt_required()
def add_test_case(suite_id) -> tuple[Response, Literal[201]]:
    suite = TestSuite.query.get_or_404(suite_id)
    data = request.get_json()
    new_case = TestCase(name=data['name'], description=data.get(
        'description', ''), test_suite_id=suite_id)
    db.session.add(new_case)
    db.session.commit()
    return jsonify(new_case.to_dict()), 201


@test_management_routes.route('/testsuites/<int:suite_id>/testcases', methods=['GET'])
@jwt_required()
def suite_test_cases(suite_id) -> Response:
    suite = TestSuite.query.get_or_404(suite_id)
    return jsonify([case.to_dict() for case in suite.test_cases])
