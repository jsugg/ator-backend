from datetime import datetime
from typing import Dict, Any
from app.utils.logger import app_logger

def format_response(status: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    response: Dict[str, Any] = {"status": status}
    if data:
        response["data"] = data
    app_logger.info(f"Response formatted: {response}")
    return response

def get_current_utc_time() -> datetime:
    current_time: datetime = datetime.utcnow()
    app_logger.info(f"Current UTC time retrieved: {current_time}")
    return current_time
