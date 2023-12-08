# In tests/test_api.py
import unittest
from app import create_app, db
from flask import Flask


class APITestCase(unittest.TestCase):
    """
    Test case class for API endpoints.
    """

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # def test_get_test_suites(self) -> None:
    #     response = self.client.get('/api/testsuites')
    #     self.assertEqual(response.status_code, 200)

    # Returns a JSON response with a message "JWT is working!" when a valid JWT token is provided.
    # def test_valid_jwt_token_with_request_context(self) -> None:
    #     app = Flask(__name__)
    #     self.client = app.test_client()

    #     valid_token = "valid_token"
    #     expected_response = {"message": "JWT is working!"}

    #     response = self.client.get('/protected', headers={'Authorization': f'Bearer {valid_token}'})

    #     assert response.status_code == 200
    #     assert response.get_json() == expected_response

    # Returns a 404 Not Found error when accessing the protected route without a JWT token.
    def test_no_jwt_token_with_client(self) -> None:
        app = Flask(__name__)
        self.client = app.test_client()

        response = self.client.get('/protected')

        assert response.status_code == 404

    # def test_non_get_request(self) -> None:
    #     response = self.client.post('/protected')

    #     assert response.status_code == 405


class TestExecutionServiceTestCase(unittest.TestCase):
    def test_execute_test_case(self) -> None:
        # Setup test data
        # Call the execute_test_case function
        # Assert the expected outcomes
        pass

    def test_execute_test_suite(self) -> None:
        # Setup test data
        # Call the execute_test_suite function
        # Assert the expected outcomes
        pass

# More tests...
