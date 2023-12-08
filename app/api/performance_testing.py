from flask_restx import Namespace, Resource, fields
from flask import jsonify, request
from app.schemas.performance_test import PerformanceTest, PerformanceTestCreate
from app.services.performance_test_service import execute_test
from app.extensions import db

performance_ns = Namespace('PerformanceTesting', description='Performance Testing Operations')

# Models
performance_test_model = performance_ns.model('PerformanceTest', {
    'name': fields.String(required=True, description='Name of the performance test'),
    'description': fields.String(description='Description of the performance test'),
    'config': fields.String(description='Configuration of the performance test')
})

performance_test_response_model = performance_ns.model('PerformanceTestResponse', {
    'id': fields.Integer(description='ID of the performance test'),
    'name': fields.String(description='Name of the performance test'),
    'description': fields.String(description='Description of the performance test'),
    'config': fields.String(description='Configuration of the performance test')
})

error_model = performance_ns.model('ErrorResponse', {
    'error': fields.String(description='Error message')
})

@performance_ns.route('/performancetests')
class PerformanceTests(Resource):
    @performance_ns.doc('get_all_performance_tests')
    @performance_ns.marshal_list_with(performance_test_response_model)
    def get(self):
        """Retrieve all performance tests."""
        tests = PerformanceTest.query.all()
        return [test.to_dict() for test in tests], 200

    @performance_ns.doc('create_performance_test')
    @performance_ns.expect(performance_test_model)
    @performance_ns.marshal_with(performance_test_response_model, code=201)
    @performance_ns.response(400, 'Invalid Request', error_model)
    def post(self):
        """Create a new performance test."""
        data = request.get_json()
        new_test = PerformanceTest(**data)
        db.session.add(new_test)
        db.session.commit()
        return new_test.to_dict(), 201


@performance_ns.route('/performancetests/<int:test_id>')
@performance_ns.param('test_id', 'The unique identifier of the performance test')
class PerformanceTestResource(Resource):
    @performance_ns.doc('get_performance_test')
    @performance_ns.marshal_with(performance_test_response_model)
    @performance_ns.response(404, 'Performance Test not found', error_model)
    def get(self, test_id):
        """Retrieve a specific performance test by its ID."""
        test = PerformanceTest.query.get_or_404(test_id)
        return test.to_dict(), 200

    @performance_ns.doc('update_performance_test')
    @performance_ns.expect(performance_test_model)
    @performance_ns.marshal_with(performance_test_response_model)
    @performance_ns.response(404, 'Performance Test not found', error_model)
    def put(self, test_id):
        """Update a specific performance test."""
        test = PerformanceTest.query.get_or_404(test_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(test, key, value)
        db.session.commit()
        return test.to_dict(), 200

    @performance_ns.doc('delete_performance_test')
    @performance_ns.response(204, 'Performance Test deleted')
    @performance_ns.response(404, 'Performance Test not found', error_model)
    def delete(self, test_id):
        """Delete a specific performance test."""
        test = PerformanceTest.query.get_or_404(test_id)
        db.session.delete(test)
        db.session.commit()
        return '', 204

performance_execution_model = performance_ns.model('PerformanceExecution', {
    'result_data': fields.Raw(description='Data resulting from performance test execution')
})

performance_results_model = performance_ns.model('PerformanceResults', {
    'id': fields.Integer(description='ID of the performance result'),
    'performance_test_id': fields.Integer(description='ID of the performance test'),
    'execution_time': fields.Float(description='Execution time of the performance test'),
    'status': fields.String(description='Status of the performance test'),
    'result_data': fields.Raw(description='Data of the performance test result')
})

@performance_ns.route('/performancetests/<int:test_id>/execute')
@performance_ns.param('test_id', 'The unique identifier of the performance test')
class ExecutePerformanceTest(Resource):
    @performance_ns.doc('execute_performance_test')
    @performance_ns.response(201, 'Performance Test Executed', performance_execution_model)
    @performance_ns.response(404, 'Performance Test not found', error_model)
    def post(self, test_id):
        """Execute a specific performance test."""
        test = PerformanceTest.query.get_or_404(test_id)
        result_data = execute_test(test)
        new_result = PerformanceResult(performance_test_id=test_id, result_data=result_data)
        db.session.add(new_result)
        db.session.commit()
        return new_result.to_dict(), 201

@performance_ns.route('/performancetests/<int:test_id>/results')
@performance_ns.param('test_id', 'The unique identifier of the performance test')
class PerformanceResults(Resource):
    @performance_ns.doc('get_performance_results')
    @performance_ns.marshal_list_with(performance_results_model)
    @performance_ns.response(200, 'Performance Test Results Retrieved')
    @performance_ns.response(404, 'Performance Test not found', error_model)
    def get(self, test_id):
        """Retrieve results of a specific performance test."""
        results = PerformanceResult.query.filter_by(performance_test_id=test_id).all()
        return [result.to_dict() for result in results], 200


@performance_ns.route('/performancetests/<int:test_id>/stop')
@performance_ns.param('test_id', 'The unique identifier of the performance test')
class StopPerformanceTest(Resource):
    @performance_ns.doc('stop_performance_test')
    @performance_ns.response(200, 'Performance Test Stopped', message_model)
    @performance_ns.response(404, 'Performance Test not found', error_model)
    def post(self, test_id):
        """Stop an ongoing performance test execution."""
        test = PerformanceTest.query.get_or_404(test_id)
        # Logic to stop the test (not detailed here)
        return {'message': f'Performance test {test_id} stopped successfully'}, 200
