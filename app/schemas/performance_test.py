from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PerformanceTestBase(BaseModel):
    """
    Base model for performance test, defining common attributes.

    Attributes:
        name (str): The name of the performance test.
        description (Optional[str]): An optional description of the performance test.
    """
    name: str
    description: Optional[str] = None

class PerformanceTestCreate(PerformanceTestBase):
    """
    Schema for creating a new performance test, extending the base model.

    Attributes:
        config (str): Configuration details for the performance test.
    """
    config: str

class PerformanceTest(PerformanceTestBase):
    """
    Schema for a performance test, including its database ID and creation time.

    Attributes:
        id (int): The unique identifier for the performance test.
        created_at (datetime): The timestamp when the test was created.

    Config:
        from_attributes (bool): Enables ORM mode for compatibility with SQLAlchemy models.
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes: bool = True
