from typing import Literal
from flask import Blueprint, Response, jsonify, request
from app.models.models import TestCase
from app import db

performance_testing_routes = Blueprint('performance_testing', __name__)

@performance_testing_routes.route('/testcases', methods=['GET', 'POST'])
def test_cases() -> Response | tuple[Response, Literal[201]] | None:
    if request.method == 'GET':
        cases = TestCase.query.all()
        return jsonify([{'id': case.id, 'name': case.name} for case in cases])
    elif request.method == 'POST':
        data = request.get_json()
        new_case = TestCase(name=data['name'], test_suite_id=data['test_suite_id'])
        db.session.add(new_case)
        db.session.commit()
        return jsonify({'id': new_case.id, 'name': new_case.name}), 201

@performance_testing_routes.route('/testcases/<int:case_id>', methods=['GET', 'PUT', 'DELETE'])
def test_case(case_id) -> Response | tuple[Response, Literal[204]] | None:
    case = TestCase.query.get_or_404(case_id)
    if request.method == 'GET':
        return jsonify({'id': case.id, 'name': case.name})
    elif request.method == 'PUT':
        data = request.get_json()
        case.name = data.get('name', case.name)
        db.session.commit()
        return jsonify({'id': case.id, 'name': case.name})
    elif request.method == 'DELETE':
        db.session.delete(case)
        db.session.commit()
        return jsonify({}), 204
