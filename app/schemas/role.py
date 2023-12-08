from pydantic import BaseModel

class RoleBase(BaseModel):
    """
    Base model for a role, defining the common attribute.

    Attributes:
        name (str): The name of the role.
    """
    name: str

class RoleCreate(RoleBase):
    """
    Schema for creating a new role.
    Inherits all attributes from RoleBase without adding additional fields.
    """
    pass

class Role(RoleBase):
    """
    Schema for a role, including its database ID.

    Attributes:
        id (int): The unique identifier for the role.

    Config:
        orm_mode (bool): Enables ORM mode for compatibility with SQLAlchemy models.
    """
    id: int

    class Config:
        orm_mode: bool = True
