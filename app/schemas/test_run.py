from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class TestRun(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    statuses: Dict[int, str]  # Mapping of test IDs to their statuses

    class Config:
        from_attributes = True
