from pydantic import BaseModel
from datetime import datetime

class PerformanceResultBase(BaseModel):
    """
    Base model for performance result, defining common attributes.

    Attributes:
        performance_test_id (int): The identifier of the associated performance test.
        execution_time (float): The time taken for the performance test execution.
        status (str): The status of the performance test result.
    """
    performance_test_id: int
    execution_time: float
    status: str

class PerformanceResultCreate(PerformanceResultBase):
    """
    Schema for creating a new performance result, extending the base model.

    Attributes:
        result_data (str): The detailed data of the performance test result.
    """
    result_data: str

class PerformanceResult(PerformanceResultBase):
    """
    Schema for a performance result, including its database ID and executed time.

    Attributes:
        id (int): The unique identifier for the performance result.
        executed_at (datetime): The timestamp when the test was executed.

    Config:
        from_attributes (bool): Enables ORM mode for compatibility with SQLAlchemy models.
    """
    id: int
    executed_at: datetime

    class Config:
        from_attributes: bool = True
