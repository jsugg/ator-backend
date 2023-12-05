from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.models import TestSuite, TestCase

test_management_routes = Blueprint('test_management', __name__)


@test_management_routes.route('/testsuites', methods=['GET', 'POST'])
@jwt_required()
def test_suites():
    if request.method == 'GET':
        suites = TestSuite.query.all()
        return jsonify([{'id': suite.id, 'name': suite.name} for suite in suites])
    elif request.method == 'POST':
        data = request.get_json()
        new_suite = TestSuite(
            name=data['name'], description=data.get('description'))
        db.session.add(new_suite)
        db.session.commit()
        return jsonify({'id': new_suite.id, 'name': new_suite.name}), 201


@test_management_routes.route('/testsuites/<int:suite_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def test_suite(suite_id):
    suite = TestSuite.query.get_or_404(suite_id)
    if request.method == 'GET':
        return jsonify({'id': suite.id, 'name': suite.name})
    elif request.method == 'PUT':
        data = request.get_json()
        suite.name = data.get('name', suite.name)
        suite.description = data.get('description', suite.description)
        db.session.commit()
        return jsonify({'id': suite.id, 'name': suite.name})
    elif request.method == 'DELETE':
        db.session.delete(suite)
        db.session.commit()
        return jsonify({}), 204


@test_management_routes.route('/testsuites', methods=['POST'])
@jwt_required()
def create_test_suite():
    # Logic to create a test suite
    pass
