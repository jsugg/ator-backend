from typing import List, Dict, Any


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
    missing_keys: List[str] = [
        key for key in required_keys if key not in json_data]
    return missing_keys
