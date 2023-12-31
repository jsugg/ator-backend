import subprocess
from typing import List, Dict, Any
from app.db.schema import TestCase, TestSuite
# from app.tasks import perform_async_test
from app.utils.logger import service_logger


def execute_test_suite(test_suite_id: int) -> Dict[str, Any]:
    """
    Executes all test cases in a given test suite.

    Args:
        test_suite_id (int): The ID of the test suite to execute.

    Returns:
        Dict[str, Any]: A dictionary containing the execution results.
    """
    test_suite = TestSuite.query.get(test_suite_id)
    if not test_suite:
        service_logger.error(f"Test Suite not found: {test_suite_id}")
        raise ValueError(f"Test Suite with ID {test_suite_id} not found.")

    results: Dict[str, Any] = {"test_suite_id": test_suite_id, "results": []}
    for test_case in test_suite.test_cases:
        result: Dict[str, Any] = execute_test_case(test_case.id)
        results["results"].append(result)

    service_logger.info(f"Executed test suite: {test_suite_id}")
    return results


def execute_test_case(test_case_id: int) -> Dict[str, Any]:
    """
    Executes a single test case using Newman.

    Args:
        test_case_id (int): The ID of the test case to execute.

    Returns:
        Dict[str, Any]: A dictionary containing the execution result.
    """
    test_case = TestCase.query.get(test_case_id)
    if not test_case:
        service_logger.error(f"Test Case not found: {test_case_id}")
        raise ValueError(f"Test Case with ID {test_case_id} not found.")

    collection_path: str = f'path_to_collections/{test_case.name}.json'
    result: subprocess.CompletedProcessa = subprocess.run(
        ["newman", "run", collection_path], capture_output=True, text=True)

    service_logger.info(
        f"Executed test case: {test_case_id}, Status: {execution_status}")
    return {
        "test_case_id": test_case_id,
        "name": test_case.name,
        "status": "success" if result.returncode == 0 else "failure",
        "output": result.stdout
    }


def aggregate_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregates results from multiple test executions.

    Args:
        results (List[Dict[str, Any]]): A list of individual test results.

    Returns:
        Dict[str, Any]: An aggregated summary of the results.
    """
    summary = {"total": len(results), "success": 0, "failure": 0}
    for result in results:
        if result["status"] == "success":
            summary["success"] += 1
        else:
            summary["failure"] += 1

    return summary


# def execute_test_case_async(test_case_id: int):
#     perform_async_test.delay(test_case_id)

    # To schedule tests, use Celery's periodic task feature or integrate with Flask's scheduling extensions.
