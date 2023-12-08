from pydantic import BaseModel
from datetime import datetime


class PerformanceResultBase(BaseModel):
    """
    Base model for performance result, defining common attributes.
    """
    performance_test_id: int
    execution_time: float
    status: str


class PerformanceResultCreate(PerformanceResultBase):
    """
    Schema for creating a new performance result, extending the base model.
    """
    result_data: str


class PerformanceResult(PerformanceResultBase):
    """
    Schema for a performance result, including its database ID and executed time.
    """
    id: int
    executed_at: datetime

    class Config:
        orm_mode: bool = True
