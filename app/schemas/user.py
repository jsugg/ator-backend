from pydantic import BaseModel

class UserBase(BaseModel):
    """
    Base model for user, defining the common attributes.

    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
    """
    username: str
    email: str

class UserCreate(UserBase):
    """
    Schema for creating a new user. Inherits all attributes from UserBase 
    and adds a password for user creation.

    Attributes:
        password (str): The password for the new user.
    """
    password: str

class User(UserBase):
    """
    Schema for a user, including its database ID.

    Attributes:
        id (int): The unique identifier for the user.
    """
    id: int

    class Config:
        orm_mode: bool = True
