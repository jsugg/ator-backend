from typing import Optional

class TestResult:
    """
    Class representing the result of a test case execution.

    Attributes:
        test_case_id (int): The ID of the test case.
        status (str): The status of the test result (e.g., 'Passed', 'Failed').
        details (Optional[str]): Additional details about the test result, if any.

    This class encapsulates the results of executing a test case, including
    the status and any additional details pertinent to the test execution.
    """

    def __init__(self, test_case_id: int, status: str, details: Optional[str] = None) -> None:
        self.test_case_id: int = test_case_id
        self.status: str = status
        self.details: Optional[str] = details

    # Additional methods for result processing or reporting can be added here
