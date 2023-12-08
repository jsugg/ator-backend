from typing import List, Optional, TypeVar, Generic
from sqlalchemy.orm import Session
from app.extensions import db
from app.db.models import TestSuite, TestCase, TestResult


T = TypeVar('T', bound=db.Model)


class BaseRepository(Generic[T]):
    """
    A base repository class for common database operations.

    Attributes:
        model (T): Generic type for the database model.

    Methods:
        get_all: Retrieve all instances of the model.
        get_by_id: Retrieve a single instance by its ID.
        add: Add a new instance to the database.
        delete: Remove an instance by its ID.
        update: Update an existing instance.
    """

    def __init__(self, model: T) -> None:
        self.model: T = model

    def get_all(self) -> List[T]:
        return self.model.query.all()

    def get_by_id(self, id: int) -> Optional[T]:
        return self.model.query.get(id)

    def add(self, entity: T) -> T:
        db.session.add(entity)
        db.session.commit()
        return entity

    def delete(self, id: int) -> None:
        entity: Optional[T] = self.get_by_id(id)
        if entity:
            db.session.delete(entity)
            db.session.commit()

    def update(self, entity: T) -> T:
        db.session.merge(entity)
        db.session.commit()
        return entity

# Example usage for a specific model (e.g., TestSuite)


class TestSuiteRepository(BaseRepository):
    """
    Repository class for TestSuite model operations.

    Inherits from BaseRepository with model-specific methods.
    """

    def __init__(self) -> None:
        super().__init__(TestSuite)


class TestCaseRepository(BaseRepository[TestCase]):
    pass


class TestResultRepository(BaseRepository[TestResult]):
    pass
