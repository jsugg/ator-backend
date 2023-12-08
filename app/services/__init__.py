from typing import Any, Literal
from prefect import flow
from app.models.models import TestSuite, User
from app.services.api_test_execution_service import aggregate_results, execute_test_case
from prefect.task_runners import ConcurrentTaskRunner


def is_user_authorized_to_execute(user_id) -> Any | Literal[False]:
    """
    Checks if the user is authorized to execute performance tests.

    :param user_id: ID of the user
    :return: Boolean indicating if the user is authorized
    """
    user: User = User.query.get(user_id)
    if not user:
        return False
    # Check user's role or permissions
    return user.is_authorized('execute_tests')


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
    test_suite: TestSuite = TestSuite.query.get(test_suite_id)
    if not test_suite:
        raise ValueError(f"Test Suite with ID {test_suite_id} not found.")

    test_case_results: dict = execute_test_case.map(
        [tc.id for tc in test_suite.test_cases])
    summary: dict[str, Any] = aggregate_results(test_case_results)
    return summary


def execute_test_suite(test_suite_id: int) -> dict[str, Any]:
    """
    Executes all test cases in a given test suite.

    Args:
        test_suite_id (int): The ID of the test suite to execute.

    Returns:
        dict[str, Any]: A dictionary containing the execution results.
    """
    test_suite: TestSuite = TestSuite.query.get(test_suite_id)
    if not test_suite:
        raise ValueError(f"Test Suite with ID {test_suite_id} not found.")

    test_case_results: dict = test_execution_flow.map([tc.id for tc in test_suite.test_cases])
    summary: dict[str, Any] = aggregate_results(test_case_results)
    return summary
