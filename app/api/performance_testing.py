import json
from typing import Literal
from flask import Blueprint, Response, abort, jsonify, request
from app.models.models import PerformanceTest, PerformanceResult
from app.services.performance_test_service import execute_performance_test
from app.db import db

performance_testing_routes = Blueprint('performance_testing', __name__)


@performance_testing_routes.route('/performancetests', methods=['GET', 'POST'])
def performance_tests() -> Response | tuple[Response, Literal[201]] | None:
    if request.method == 'GET':
        tests = PerformanceTest.query.all()
        return jsonify([test.to_dict() for test in tests]), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_test = PerformanceTest(**data)
        db.session.add(new_test)
        db.session.commit()
        return jsonify(new_test.to_dict()), 201


@performance_testing_routes.route('/performancetests/<int:test_id>', methods=['GET', 'PUT', 'DELETE'])
def performance_test(test_id) -> Response | tuple[Response, Literal[204]] | None:
    test = PerformanceTest.query.get_or_404(test_id)

    if request.method == 'GET':
        return jsonify(test.to_dict()), 200

    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(test, key, value)
        db.session.commit()
        return jsonify(test.to_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(test)
        db.session.commit()
        return jsonify({}), 204


@performance_testing_routes.route('/performancetests/<int:test_id>/execute', methods=['POST'])
def execute_performance(test_id) -> Response:
    test = PerformanceTest.query.get_or_404(test_id)
    result_data = execute_performance_test(test)
    new_result = PerformanceResult(
        performance_test_id=test_id, result_data=result_data)
    db.session.add(new_result)
    db.session.commit()
    return jsonify(new_result.to_dict()), 201


@performance_testing_routes.route('/performancetests/<int:test_id>/results', methods=['GET'])
def performance_results(test_id) -> Response:
    results = PerformanceResult.query.filter_by(
        performance_test_id=test_id).all()
    return jsonify([result.to_dict() for result in results]), 200
