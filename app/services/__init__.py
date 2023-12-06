from typing import Any, Literal
from .api_test_execution_service import *
from .performance_test_service import *
from flask_jwt_extended import get_jwt_identity
from app.models.models import User

def is_user_authorized_to_execute(user_id) -> Any | Literal[False]:
    """
    Checks if the user is authorized to execute performance tests.

    :param user_id: ID of the user
    :return: Boolean indicating if the user is authorized
    """
    user = User.query.get(user_id)
    if not user:
        return False
    # Check user's role or permissions
    return user.is_authorized('execute_tests')


def send_notification(message) -> None:
    """
    Sends a notification with the given message.

    :param message: Message to be sent in the notification
    """
    # Placeholder for notification logic
    # This could be an email, Slack message, webhook, etc.
    print(f"Notification: {message}")
