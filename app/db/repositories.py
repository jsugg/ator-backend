from typing import List, Optional, TypeVar, Generic
from sqlalchemy.orm import Session
from app.extensions import db
from app.db.models import TestSuite, TestCase, TestResult
from app.utils.logger import db_logger  # Assuming db_logger is correctly configured

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
        try:
            results = self.model.query.all()
            db_logger.info(f"Retrieved all records for {self.model.__name__}.")
            return results
        except Exception as e:
            db_logger.error(f"Error retrieving all records for {self.model.__name__}: {str(e)}")
            return []

    def get_by_id(self, id: int) -> Optional[T]:
        try:
            entity = self.model.query.get(id)
            if entity:
                db_logger.info(f"Retrieved record with ID {id} for {self.model.__name__}.")
            else:
                db_logger.warning(f"No record found with ID {id} for {self.model.__name__}.")
            return entity
        except Exception as e:
            db_logger.error(f"Error retrieving record with ID {id} for {self.model.__name__}: {str(e)}")
            return None

    def add(self, entity: T) -> T:
        try:
            db.session.add(entity)
            db.session.commit()
            db_logger.info(f"Added new record for {self.model.__name__}.")
            return entity
        except Exception as e:
            db_logger.error(f"Error adding new record for {self.model.__name__}: {str(e)}")
            return None

    def delete(self, id: int) -> None:
        try:
            entity: Optional[T] = self.get_by_id(id)
            if entity:
                db.session.delete(entity)
                db.session.commit()
                db_logger.info(f"Deleted record with ID {id} for {self.model.__name__}.")
        except Exception as e:
            db_logger.error(f"Error deleting record with ID {id} for {self.model.__name__}: {str(e)}")

    def update(self, entity: T) -> T:
        try:
            db.session.merge(entity)
            db.session.commit()
            db_logger.info(f"Updated record for {self.model.__name__}.")
            return entity
        except Exception as e:
            db_logger.error(f"Error updating record for {self.model.__name__}: {str(e)}")
            return None

class TestSuiteRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(TestSuite)

class TestCaseRepository(BaseRepository[TestCase]):
    pass

class TestResultRepository(BaseRepository[TestResult]):
    pass
