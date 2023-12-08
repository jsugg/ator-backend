import pytest
from app.db.models import User

def test_new_user(new_user) -> None:
    """
    Test the creation of a new user.

    Args:
        new_user: The user fixture for testing.

    Asserts:
        The correctness of the created user attributes.
    """
    assert new_user.username == 'testuser'
    assert new_user.email == 'test@example.com'
    assert new_user.password_hash is not None
