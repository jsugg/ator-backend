from typing import Any, Literal
from prefect import flow
from app.db.schema import TestSuite, User
from app.services.api_test_execution_service import aggregate_results, execute_test_case
from prefect.task_runners import ConcurrentTaskRunner
from app.utils.logger import service_logger


def is_user_authorized_to_execute(user_id) -> Any | Literal[False]:
    """
    Checks if the user is authorized to execute performance tests.

    :param user_id: ID of the user
    :return: Boolean indicating if the user is authorized
    """
    try:
        user: User = User.query.get(user_id)
        if not user:
            return False
        # Check user's role or permissions
        # Example: user.is_authorized('admin'), user.is_authorized('read_only'), user.is_authorized('execute_tests'), etc.

        return user.is_authorized('execute_tests')
    
    except Exception as err:
        service_logger.error(f"Error checking user authorization: {err}")
        return False



def send_notification(message) -> None:
    """
    Sends a notification with the given message.

    :param message: Message to be sent in the notification
    """
    # Placeholder for notification logic
    # This could be an email, Slack message, webhook, etc.
    print(f"Notification: {message}")


@flow(task_runner=ConcurrentTaskRunner())
def test_execution_flow(test_suite_id: int):
    """
    Flow to execute a test suite and aggregate results.

    Args:
        test_suite_id (int): The ID of the test suite to execute.
    """
    try:
        test_suite: TestSuite = TestSuite.query.get(test_suite_id)
    
    except Exception as err:
        service_logger.error(f"Error retrieving test suite {test_suite_id}: {err}")
        raise err

    if not test_suite:
        service_logger.info(f"Test suite {test_suite_id} not found")
        raise ValueError(f"Test suite with ID {test_suite_id} not found.")

    test_case_results: dict = {}

    try:
        for tc in test_suite.test_cases:
            service_logger.info(f"Executing test case: {tc.id}")
            test_case_results.update({tc.id: execute_test_case(tc.id)})

        service_logger.info(f"Executed test suite: {test_suite_id}")
        summary: dict[str, Any] = aggregate_results(test_case_results)
        return summary

    except Exception as err:
        service_logger.error(f"Error executing test suite {test_suite_id}: {err}")
        raise err


def execute_test_suite(test_suite_id: int) -> dict[str, Any]:
    """
    Executes all test cases in a given test suite.

    Args:
        test_suite_id (int): The ID of the test suite to execute.

    Returns:
        dict[str, Any]: A dictionary containing the execution results.
    """
    try:
        test_suite: TestSuite = TestSuite.query.get(test_suite_id)
        if not test_suite:
            service_logger.error(f"Test Suite not found: {test_suite_id}")
            raise ValueError(f"Test Suite with ID {test_suite_id} not found.")
        
    except Exception as err:
        service_logger.error(f"Error retrieving test suite {test_suite_id}: {err}")
        raise err

    try:
        test_case_results: dict = test_execution_flow.map([tc.id for tc in test_suite.test_cases])
        summary: dict[str, Any] = aggregate_results(test_case_results)
        return summary
    
    except Exception as err:
        service_logger.error(f"Error executing test suite {test_suite_id}: {err}")
        raise err
