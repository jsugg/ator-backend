from typing import Literal
from flask import Blueprint, Response, abort, request, jsonify
from flask_jwt_extended import jwt_required
from app.db.schema import TestSuite, TestCase, TestResult
from app.extensions import db
from app.services.api_test_execution_service import execute_test_suite, execute_test_case
from app.utils.logger import api_logger


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
        try:
            api_logger.info("Retrieving test suites")
            suites: list[TestSuite] = TestSuite.query.all()
            if not suites:
                api_logger.info("No test suites found")
                return jsonify([]), 200
            api_logger.info(f"Found {len(suites)} test suites")
            return jsonify([suite.to_dict() for suite in suites]), 200
        except Exception as e:
            api_logger.error(f"Error retrieving test suites: {e}")
            return jsonify({"error": str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_suite = TestSuite(
                name=data['name'], description=data.get('description', ''))
            db.session.add(new_suite)
            db.session.commit()
            api_logger.info(f"Added new test suite: {new_suite.name}")
            return jsonify(new_suite.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            api_logger.error(f"Error creating test suite: {e}")
            return jsonify({"error": str(e)}), 500

    return None


@test_management_routes.route('/testsuites/<int:suite_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def test_suite(suite_id) -> Response | tuple[Response, Literal[204]] | None:
    """
    Retrieves, updates, or deletes a test suite.

    Parameters:
    - suite_id (int): The ID of the test suite to retrieve, update, or delete.

    Returns:
    - Response: If the request method is GET or PUT, returns a JSON response containing the test suite details.
    - tuple[Response, Literal[204]]: If the request method is DELETE, returns an empty JSON response with status code 204.
    - None: If the request method is not supported.
    """
    try:
        suite: TestSuite = TestSuite.query.get_or_404(suite_id)
        api_logger.info(f"Found test suite: {suite.name}")

    except Exception as err:
        api_logger.error(f"Error retrieving test suite {suite_id}: {err}")
        abort(
            500, description=f"Error retrieving test suite {suite_id}: {err}")

    if request.method == 'GET':
        api_logger.info(f"Retrieving test suite: {suite_id}")
        return jsonify(suite.to_dict())

    elif request.method == 'PUT':
        try:
            data: dict[str, str] = request.get_json()
            suite.name: str = data.get('name', suite.name)
            suite.description: str = data.get('description', suite.description)
            db.session.commit()
            api_logger.info(f"Updated test suite: {suite_id}")
            return jsonify(suite.to_dict())

        except Exception as err:
            api_logger.error(f"Error updating test suite {suite_id}: {err}")
            abort(
                500, description=f"Error updating test suite {suite_id}: {err}")

    elif request.method == 'DELETE':
        try:
            db.session.delete(suite)
            db.session.commit()
            api_logger.info(f"Deleted test suite: {suite_id}")
            return jsonify({}), 204

        except Exception as err:
            api_logger.error(f"Error deleting test suite {suite_id}: {err}")
            abort(
                500, description=f"Error deleting test suite {suite_id}: {err}")


@test_management_routes.route('/testsuites/<int:suite_id>/execute', methods=['POST'])
@jwt_required()
def execute_suite(suite_id) -> tuple[Response, Literal[200]] | tuple[Response, Literal[404]]:
    """
    Executes a test suite.

    Parameters:
        suite_id (int): The ID of the test suite to execute.

    Returns:
        tuple[Response, Literal[200]] | tuple[Response, Literal[404]]: A tuple containing a Flask Response object and a status code. If the test suite execution is successful, the response will contain the results of the execution and the status code will be 200. If the test suite does not exist, the response will contain an error message and the status code will be 404.
    """
    try:
        results: list[TestResult] | None = execute_test_suite(suite_id)
        if not results:
            api_logger.info(f"Test suite {suite_id} not found")
            return jsonify({"error": "Test suite not found"}), 404
        api_logger.info(f"Executed test suite {suite_id}")
        return jsonify(results), 200

    except ValueError as e:
        api_logger.error(f"Error executing test suite {suite_id}: {e}")
        return jsonify({"error": str(e)}), 404


@test_management_routes.route('/testcases', methods=['GET', 'POST'])
def test_cases() -> Response | tuple[Response, Literal[201]] | None:
    """
    Route handler for '/testcases' endpoint.

    Handles GET and POST requests.

    Parameters:
        None

    Returns:
        - If the request method is GET:
            - A JSON response containing a list of all test cases and status code 200.
        - If the request method is POST:
            - A JSON response containing the newly created test case and status code 201.

    Return Types:
        - If the request method is GET:
            - Response
        - If the request method is POST:
            - Tuple[Response, Literal[201]]
        - If the request method is neither GET nor POST:
            - None
    """
    if request.method == 'GET':
        try:
            cases: list[TestCase] = TestCase.query.all()
            if not cases:
                api_logger.info("No test cases found")
                return jsonify([]), 200
            api_logger.info("Fetched all test cases")
            return jsonify([case.to_dict() for case in cases]), 200

        except Exception as err:
            api_logger.error(f"Error fetching test cases: {err}")
            return jsonify({"error": str(e)}), 400

    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_case: TestCase = TestCase(**data)
            db.session.add(new_case)
            db.session.commit()
            api_logger.info(f"Added new test case: {new_case.name}")
            return jsonify(new_case.to_dict()), 201

        except Exception as e:
            api_logger.error(f"Error adding new test case: {e}")
            return jsonify({"error": str(e)}), 400


@test_management_routes.route('/testsuites/<int:suite_id>/testcases', methods=['POST'])
@jwt_required()
def add_test_case_to_suite(suite_id) -> tuple[Response, Literal[201]]:
    """
    Add a test case to a test suite.

    Args:
        suite_id (int): The ID of the test suite.

    Returns:
        tuple[Response, Literal[201]]: A tuple containing the response object and the HTTP status code 201.

    Raises:
        404: If the test suite is not found.

    """
    try:
        suite = TestSuite.query.get_or_404(suite_id)
        if not suite:
            api_logger.info(f"Test suite {suite_id} not found")
            abort(404, description="Test suite not found.")

        data = request.get_json()
        new_case = TestCase(name=data['name'], description=data.get(
            'description', ''), test_suite_id=suite_id)
        db.session.add(new_case)
        db.session.commit()
        api_logger.info(
            f"Added new test case {new_case.name} to test suite {suite_id}")

    except ValueError as err:
        api_logger.error(
            f"Error adding test case to test suite {suite_id}: {err}")
        abort(
            400, description=f"Error adding test case to test suite {suite_id}: {err}")

    except Exception as err:
        api_logger.error(
            f"Error adding test case to test suite {suite_id}: {err}")
        db.session.rollback()
        abort(
            500, description=f"Error adding test case to test suite {suite_id}: {err}")
        raise err
    return jsonify(new_case.to_dict()), 201


@test_management_routes.route('/testcases/<int:case_id>', methods=['GET', 'PUT', 'DELETE'])
def test_case(case_id) -> Response | tuple[Response, Literal[204]] | None:
    """
    Retrieves, updates, or deletes a test case by its ID.

    Args:
        case_id (int): The ID of the test case.

    Returns:
        - Response: If the request method is GET or PUT, a JSON response containing the test case ID and name, with a status code of 200.
        - tuple[Response, Literal[204]]: If the request method is DELETE, an empty JSON response with a status code of 204.
        - None: If the request method is not GET, PUT, or DELETE.

    Raises:
        400 Bad Request: If the request method is PUT and no data is provided.
        404 Not Found: If the test case with the given ID does not exist.
        405 Method Not Allowed: If the request method is not GET, PUT, or DELETE.

    """
    try:
        case = TestCase.query.get_or_404(case_id)
        api_logger.info(f"Retrieved test case {case.name} with ID {case.id}")

    except Exception as err:
        api_logger.error(f"Error retrieving test case {case_id}: {err}")
        abort(500, description=f"Error retrieving test case {case_id}: {err}")

    if request.method == 'GET':
        return jsonify({'id': case.id, 'name': case.name}), 200

    if request.method == 'PUT':
        try:
            data = request.get_json()
            case.name = data.get('name', case.name)
            case.description = data.get('description', case.description)
            db.session.commit()
            api_logger.info(f"Updated test case {case.name} with ID {case.id}")
            return jsonify({'id': case.id, 'name': case.name}), 200

        except Exception as err:
            db.session.rollback()
            api_logger.error(
                f"Error updating test case {case.name} with ID {case.id}: {err}")
            return jsonify({"error": str(err)}), 400

    if request.method == 'DELETE':
        try:
            db.session.delete(case)
            db.session.commit()
            api_logger.info(f"Deleted test case {case.name} with ID {case.id}")
            return jsonify({}), 204

        except Exception as err:
            db.session.rollback()
            api_logger.error(
                f"Error deleting test case {case.name} with ID {case.id}: {err}")
            return jsonify({"error": str(err)}), 400

    return jsonify(error="Method Not Allowed"), 405


@test_management_routes.route('/testcases/<int:case_id>/execute', methods=['GET', 'POST'])
def test_case_execution(case_id) -> Response:
    """
    Execute a test case.

    Args:
        case_id (int): The ID of the test case to execute.

    Returns:
        Response: The response object containing the test case execution status.
    """
    if request.method == 'GET':
        # Retrieve the current test case execution status
        try:
            case = TestCase.query.get_or_404(case_id)
            api_logger.info(
                f"Retrieved test case {case.name} with ID {case.id}")

        except Exception as err:
            api_logger.error(f"Error retrieving test case {case_id}: {err}")
            return jsonify(error=str(err)), 404

        try:
            result = TestResult.query.filter_by(test_case_id=case_id).first()
            if result:
                api_logger.info(
                    f"Retrieved test case execution for test case {case.name} with ID {case.id}")
                return jsonify(result.to_dict()), 200
            else:
                api_logger.info(
                    f"Test case execution not found for test case {case.name} with ID {case.id}")
                return jsonify(error="Test case execution not found"), 404
        except Exception as err:
            api_logger.error(
                f"Error retrieving test case execution for test case {case.name} with ID {case.id}: {err}")
            return jsonify(error=str(err)), 500

    elif request.method == 'POST':
        # Execute the test case
        try:
            case = TestCase.query.get_or_404(case_id)
            result = execute_test_case(case)
            new_result = TestResult(test_case_id=case_id, result_data=result)
            db.session.add(new_result)
            db.session.commit()
            api_logger.info(
                f"Executed test case {case.name} with ID {case.id}")
            return jsonify(new_result.to_dict()), 201

        except Exception as err:
            db.session.rollback()
            api_logger.error(
                f"Error executing test case {case.name} with ID {case.id}: {err}")
            return jsonify(error=str(err)), 500


@test_management_routes.route('/testcases/<int:case_id>/results', methods=['GET'])
def get_test_case_results(case_id) -> Response | tuple[Response, Literal[200]] | None:
    """
    Get the test case results for a specific case ID.

    Args:
        case_id (int): The ID of the test case.

    Returns:
        Response | tuple[Response, Literal[200]] | None: The test case results as a JSON object and the HTTP status code 200 if successful, or None if the test case does not exist.
    """
    try:
        case = TestCase.query.get_or_404(case_id)
        if not case:
            api_logger.info(f"Test case {case_id} not found")
            return jsonify(error="Test case not found"), 404

        api_logger.info(f"Retrieved test case results for test case {case_id}")
        return jsonify(case.to_dict()), 200

    except Exception as err:
        api_logger.error(
            f"Error retrieving test case results for test case {case_id}: {err}")
        return jsonify(error=str(err)), 500


@test_management_routes.route('/testcases/<int:case_id>/results', methods=['GET'])
def results(case_id) -> Response:
    """
    Get the results for a specific test case.

    Parameters:
        case_id (int): The ID of the test case.

    Returns:
        Response: A JSON response containing the results of the test case.
    """
    try:
        results = TestResult.query.filter_by(test_case_id=case_id).all()
        if not results:
            api_logger.info(f"No results found for test case {case_id}")
            return jsonify(error="No results found"), 404

        api_logger.info(f"Retrieved results for test case {case_id}")
        return jsonify([result.to_dict() for result in results]), 200

    except Exception as err:
        api_logger.error(
            f"Error retrieving results for test case {case_id}: {err}")
        return jsonify(error=str(err)), 500
