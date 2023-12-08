from typing import Any, Dict, List

class TestCase:
    """
    Class representing a test case.

    Attributes:
        id (int): The unique identifier of the test case.
        name (str): The name of the test case.
        steps (List[Dict[str, Any]]): The steps involved in the test case.

    This class encapsulates the details of a test case, including its identifier,
    name, and the steps that constitute the test case.
    """

    def __init__(self, id: int, name: str, steps: List[Dict[str, Any]]) -> None:
        self.id: int = id
        self.name: str = name
        self.steps: List[Dict[str, Any]] = steps

    # Additional methods for test case execution or manipulation can be added here
