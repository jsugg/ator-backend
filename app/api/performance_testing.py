from typing import Any, Literal
from flask_restx import Namespace, Resource, fields
from flask import Blueprint, request
from app.schemas.performance_test import PerformanceTest
from app.schemas.performance_result import PerformanceResult
from app.schemas.test_run import TestRun
from app.services.performance_test_service import LocustPerformanceTester
from app.extensions import db
from app.utils.logger import api_logger

performance_testing_routes = Blueprint('performance_testing', __name__)

# Namespace
performance_testing_ns = Namespace(
    'PerformanceTesting', description='Performance Testing Operations')

# Models
performance_test_model = performance_testing_ns.model('PerformanceTest', {
    'name': fields.String(required=True, description='Name of the performance test'),
    'description': fields.String(description='Description of the performance test'),
    'config': fields.String(description='Configuration of the performance test')
})

performance_test_response_model = performance_testing_ns.model('PerformanceTestResponse', {
    'id': fields.Integer(description='ID of the performance test'),
    'name': fields.String(description='Name of the performance test'),
    'description': fields.String(description='Description of the performance test'),
    'config': fields.String(description='Configuration of the performance test')
})

error_model = performance_testing_ns.model('ErrorResponse', {
    'error': fields.String(description='Error message')
})

message_model = performance_testing_ns.model('MessageResponse', {
    'message': fields.String(description='Response message')
})


@performance_testing_routes.route('/performancetests')
class PerformanceTests(Resource):
    """
    This class provides API endpoints for managing and retrieving performance tests. 

    It supports:
        GET: Retrieve all performance tests.
        POST: Create a new performance test.
    """
    @performance_testing_ns.doc('get_all_performance_tests')
    @performance_testing_ns.marshal_list_with(performance_test_response_model)
    def get(self) -> tuple[list, Literal[200]]:
        """Retrieve all performance tests."""
        tests: list[PerformanceTest]

        try:
            tests = PerformanceTest.query.all()
            api_logger.info(f"Fetched {len(tests)} performance tests")
        except Exception as err:
            api_logger.error(f"Error fetching performance tests: {err}")
            return {'error': str(err)}, 500

        if not tests:
            api_logger.info("No performance tests found")
            return [], 200

        return [test.to_dict() for test in tests], 200

    @performance_testing_ns.doc('create_performance_test')
    @performance_testing_ns.expect(performance_test_model)
    @performance_testing_ns.marshal_with(performance_test_response_model, code=201)
    @performance_testing_ns.response(400, 'Invalid Request', error_model)
    def post(self) -> tuple[Any, Literal[201]]:
        try:
            """Create a new performance test."""
            data = request.get_json()
            new_test = PerformanceTest(**data)
            db.session.add(new_test)
            db.session.commit()
            api_logger.info(f"Added new performance test: {new_test.name}")
            return new_test.to_dict(), 201

        except Exception as err:
            db.session.rollback()
            api_logger.error(f"Error creating performance test: {err}")
            return {'error': str(err)}, 500


@performance_testing_routes.route('/performancetests/<int:test_id>')
@performance_testing_ns.param('test_id', 'The unique identifier of the performance test')
class PerformanceTestResource(Resource):
    """
    This class provides API endpoints for managing and retrieving performance tests. 

    It supports:
        GET: Retrieve a specific performance test by its ID.
        PUT: Update a specific performance test.
        DELETE: Delete a specific performance test.
    """

    @performance_testing_ns.expect(performance_test_model)
    @performance_testing_ns.doc('get_performance_test')
    @performance_testing_ns.marshal_with(performance_test_response_model)
    @performance_testing_ns.response(404, 'Performance Test not found', error_model)
    def get(self, test_id):
        """Retrieve a specific performance test by its ID."""
        test: PerformanceTest

        try:
            test = PerformanceTest.query.get_or_404(test_id)
        except Exception as err:
            api_logger.error(
                f"Error retrieving performance test {test_id}: {err}")
            return {'error': str(err)}, 404

        api_logger.info(f"Retrieved performance test: {test.name}")
        return test.to_dict(), 200

    @performance_testing_ns.doc('update_performance_test')
    @performance_testing_ns.expect(performance_test_model)
    @performance_testing_ns.marshal_with(performance_test_response_model)
    @performance_testing_ns.response(404, 'Performance Test not found', error_model)
    def put(self, test_id):
        test: PerformanceTest
        try:
            """Update a specific performance test."""
            test = PerformanceTest.query.get_or_404(test_id)
            data = request.get_json()
            for key, value in data.items():
                setattr(test, key, value)
            db.session.commit()
            return test.to_dict(), 200

        except Exception as err:
            db.session.rollback()
            api_logger.error(
                f"Error updating performance test {test_id}: {err}")
            return {'error': str(err)}, 500

    @performance_testing_ns.doc('delete_performance_test')
    @performance_testing_ns.response(204, 'Performance Test deleted')
    @performance_testing_ns.response(404, 'Performance Test not found', error_model)
    def delete(self, test_id):
        test: PerformanceTest
        try:
            """Delete a specific performance test."""
            test = PerformanceTest.query.get_or_404(test_id)
            db.session.delete(test)
            db.session.commit()
            return '', 204

        except Exception as err:
            db.session.rollback()
            api_logger.error(
                f"Error deleting performance test {test_id}: {err}")
            return {'error': str(err)}, 500


performance_execution_model = performance_testing_ns.model('PerformanceExecution', {
    'result_data': fields.Raw(description='Data resulting from performance test execution')
})

performance_results_model = performance_testing_ns.model('PerformanceResults', {
    'id': fields.Integer(description='ID of the performance result'),
    'performance_test_id': fields.Integer(description='ID of the performance test'),
    'execution_time': fields.Float(description='Execution time of the performance test'),
    'status': fields.String(description='Status of the performance test'),
    'result_data': fields.Raw(description='Data of the performance test result')
})


@performance_testing_routes.route('/performancetests/<int:test_id>/execute')
@performance_testing_ns.param('test_id', 'The unique identifier of the performance test')
class ExecutePerformanceTest(Resource):
    @performance_testing_ns.doc('execute_performance_test')
    @performance_testing_ns.response(201, 'Performance Test Executed', performance_execution_model)
    @performance_testing_ns.response(404, 'Performance Test not found', error_model)
    def post(self, test_id) -> tuple[Any, Literal[201]]:
        try:
            """Execute a specific performance test."""
            test: PerformanceTest = PerformanceTest.query.get_or_404(test_id)
            performance_tester: LocustPerformanceTester = LocustPerformanceTester(
                db.session)
            result_data: dict[str, Any] | None = performance_tester.execute_test(
                performance_test_id=test.id)
            new_result: PerformanceResult = PerformanceResult(
                performance_test_id=test_id, result_data=result_data)
            db.session.add(new_result)
            db.session.commit()
            return new_result.to_dict(), 201

        except Exception as err:
            db.session.rollback()
            api_logger.error(f"Error executing performance test: {err}")
            return {'error': str(err)}, 500


@performance_testing_routes.route('/performancetests/<int:test_id>/results')
@performance_testing_ns.param('test_id', 'The unique identifier of the performance test')
class PerformanceTestResults(Resource):
    @performance_testing_ns.doc('get_performance_results')
    @performance_testing_ns.marshal_list_with(performance_results_model)
    @performance_testing_ns.response(200, 'Performance Test Results Retrieved')
    @performance_testing_ns.response(404, 'Performance Test not found', error_model)
    def get(self, test_id) -> tuple[list, Literal[200]]:
        try:
            """Retrieve results of a specific performance test."""
            results = PerformanceResult.query.filter_by(
                performance_test_id=test_id).all()
            return [result.to_dict() for result in results], 200
        except Exception as err:
            api_logger.error(f"Error retrieving performance results: {err}")
            return {'error': str(err)}, 500


@performance_testing_routes.route('/performancetests/<int:test_id>/stop')
@performance_testing_ns.param('test_id', 'The unique identifier of the performance test')
class StopPerformanceTest(Resource):
    @performance_testing_ns.doc('stop_performance_test')
    @performance_testing_ns.response(200, 'Performance Test Stopped', message_model)
    @performance_testing_ns.response(404, 'Performance Test not found', error_model)
    def post(self, test_id) -> tuple[dict[str, str], Literal[200]]:
        try:
            """Stop a specific performance test."""
            test = PerformanceTest.query.get_or_404(test_id)
            # TODO: Logic to stop the test
            api_logger.info(f"Stopped performance test: {test.name}")
            return {'message': f'Performance test {test_id} stopped successfully'}, 200

        except Exception as err:
            api_logger.error(f"Error stopping performance test: {err}")
            return {'error': str(err)}, 500
