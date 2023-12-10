from typing import List, Dict, Any
from app.utils.logger import app_logger


def validate_json(required_keys: List[str], json_data: Dict[str, Any]) -> List[str]:
    """
    Validate if all required keys are present in the provided JSON data.

    Args:
        required_keys (List[str]): A list of keys that are required in the JSON data.
        json_data (Dict[str, Any]): The JSON data to validate.

    Returns:
        List[str]: A list of missing keys, if any.

    This function checks whether the provided JSON data contains all the required keys.
    It returns a list of missing keys if any are found. If no keys are missing, it returns an empty list.
    """
    try:
        missing_keys: List[str] = [
            key for key in required_keys if key not in json_data]
        if missing_keys:
            app_logger.error(f"Missing required keys: {missing_keys}")
        else:
            app_logger.info("JSON data is valid")
        return missing_keys
    except Exception as err:
        app_logger.error(f"Error validating JSON data: {err}")
        raise err


def generate_unique_identifier() -> str:
    """
    Generates a unique identifier using the `uuid4` function from the `uuid` module.

    :return: A string representing the generated unique identifier.
    :rtype: str
    """
    from uuid import uuid4
    unique_id: str = str(uuid4())
    return unique_id
