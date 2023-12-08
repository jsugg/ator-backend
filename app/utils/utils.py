from datetime import datetime

def get_current_time() -> datetime:
    """
    Retrieve the current UTC time.

    Returns:
        datetime: The current UTC time.

    This function fetches the current UTC time, which can be used throughout the application
    for timestamping, logging, or any other purpose requiring the current time.
    """
    return datetime.utcnow()
