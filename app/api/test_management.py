from typing import Literal
from flask import Blueprint, Response, abort, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.models import TestSuite, TestCase, TestResult
from app.extensions import db
from app.services.api_test_execution_service import execute_test_suite, execute_test_case

test_management_routes = Blueprint('test_management', __name__)


@test_management_routes.route('/testsuites', methods=['GET', 'POST'])
@jwt_required()
def test_suites() -> Response | tuple[Response, Literal[201]] | None:
    """
    Retrieve or create test suites.

    Returns:
        Tuple[jsonify, int]: A JSON response with the test suites data and the HTTP status code.
    """
    if request.method == 'GET':
        return jsonify([suite.to_dict() for suite in TestSuite.query.all()]), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_suite = TestSuite(
            name=data['name'], description=data.get('description', ''))
        db.session.add(new_suite)
        db.session.commit()
        return jsonify(new_suite.to_dict()), 201
    
    return None

@test_management_routes.route('/testsuites/<int:suite_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def test_suite(suite_id) -> Response | tuple[Response, Literal[204]] | None:
    suite: TestSuite = TestSuite.query.get_or_404(suite_id)

    if request.method == 'GET':
        return jsonify(suite.to_dict())

    elif request.method == 'PUT':
        data: dict[str, str] = request.get_json()
        suite.name: str = data.get('name', suite.name)
        suite.description: str = data.get('description', suite.description)
        db.session.commit()
        return jsonify(suite.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(suite)
        db.session.commit()
        return jsonify({}), 204


@test_management_routes.route('/testsuites/<int:suite_id>/execute', methods=['POST'])
@jwt_required()
def execute_suite(suite_id) -> tuple[Response, Literal[200]] | tuple[Response, Literal[404]]:
    try:
        results = execute_test_suite(suite_id)
        return jsonify(results), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@test_management_routes.route('/testcases', methods=['GET', 'POST'])
def test_cases() -> Response | tuple[Response, Literal[201]] | None:
    if request.method == 'GET':
        cases: list[TestCase] = TestCase.query.all()
        return jsonify([case.to_dict() for case in cases]), 200
    elif request.method == 'POST':
        data = request.get_json()
        new_case: TestCase = TestCase(**data)
        db.session.add(new_case)
        db.session.commit()
        return jsonify(new_case.to_dict()), 201


@test_management_routes.route('/testsuites/<int:suite_id>/testcases', methods=['POST'])
@jwt_required()
def add_test_case_to_suite(suite_id) -> tuple[Response, Literal[201]]:
    suite = TestSuite.query.get_or_404(suite_id)
    if not suite:
        abort(404, description="Test suite not found.")

    data = request.get_json()
    new_case = TestCase(name=data['name'], description=data.get('description', ''), test_suite_id=suite_id)
    db.session.add(new_case)
    db.session.commit()
    return jsonify(new_case.to_dict()), 201


@test_management_routes.route('/testcases/<int:case_id>', methods=['GET', 'PUT', 'DELETE'])
def test_case(case_id) -> Response | tuple[Response, Literal[204]] | None:
    case = TestCase.query.get_or_404(case_id)
    if request.method == 'GET':
        return jsonify({'id': case.id, 'name': case.name}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, description="No data provided.")
        for key, value in data.items():
            if hasattr(case, key):
                setattr(case, key, value)
        db.session.commit()
        return jsonify(case.to_dict()), 200
    elif request.method == 'DELETE':
        db.session.delete(case)
        db.session.commit()
        return jsonify({}), 204
    else:
        return jsonify(error="Method Not Allowed"), 405


@test_management_routes.route('/testcases/<int:case_id>/execute', methods=['GET', 'POST'])
def test_case_execution(case_id) -> Response:
    if request.method == 'GET':
        # Retrieve the current test case execution status
        result = TestResult.query.filter_by(test_case_id=case_id).first()
        if result:
            return jsonify(result.to_dict()), 200
        else:
            return jsonify(error="Test case execution not found"), 404
    elif request.method == 'POST':
        case = TestCase.query.get_or_404(case_id)
        result = execute_test_case(case)
        new_result = TestResult(test_case_id=case_id, result_data=result)
        db.session.add(new_result)
        db.session.commit()
        return jsonify(new_result.to_dict()), 201


@test_management_routes.route('/testcases/<int:case_id>/results', methods=['GET', 'POST'])
def get_test_case_results(case_id) -> Response | tuple[Response, Literal[200]] | None:
    case = TestCase.query.get_or_404(case_id)
    return jsonify(case.to_dict()), 200


@test_management_routes.route('/testcases/<int:case_id>/results', methods=['GET'])
def results(case_id) -> Response:
    results = TestResult.query.filter_by(test_case_id=case_id).all()
    return jsonify([result.to_dict() for result in results]), 200
