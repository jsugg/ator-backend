from typing import Dict, Any
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, Mapped, DeclarativeBase, MappedAsDataclass
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from app.utils.logger import db_logger
from app.extensions import db


class BaseSchema(DeclarativeBase, MappedAsDataclass):
    pass


class TestSuite(BaseSchema):
    __tablename__ = 'test_suites'

    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String(128), nullable=False)
    description: Column = Column(String(256), nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert TestSuite instance to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the TestSuite instance.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "test_cases": [test_case.to_dict() for test_case in self.test_cases]
        }

    def save(self) -> None:
        """
        Save the object to the database.

        This method adds the object to the session, commits the changes, and logs the result.
        If an error occurs during the save process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.add(self)
            db.session.commit()
            db_logger.info(f"TestSuite saved: {self.name}")
        except Exception as err:
            db_logger.error(f"Error saving TestSuite: {err}")

    def delete(self) -> None:
        """
        Delete the object from the database.

        This method removes the object from the session, commits the changes, and logs the result.
        If an error occurs during the delete process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
            db_logger.info(f"TestSuite deleted: {self.name}")
        except Exception as err:
            db_logger.error(f"Error deleting TestSuite: {err}")


class TestCase(BaseSchema):
    __tablename__ = 'test_cases'

    id: Column = Column(Integer, primary_key=True)
    test_suite_id: Column = Column(
        Integer, ForeignKey('test_suites.id'), nullable=False)
    name: Column = Column(String(128), nullable=False)
    description: Column = Column(String(256), nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert TestCase instance to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the TestCase instance.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "test_suite_id": self.test_suite_id
        }

    def save(self) -> None:
        """
        Save the object to the database.

        This method adds the object to the session, commits the changes, and logs the result.
        If an error occurs during the save process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.add(self)
            db.session.commit()
            db_logger.info(f"TestCase saved: {self.name}")
        except Exception as err:
            db_logger.error(f"Error saving TestCase: {err}")

    def delete(self) -> None:
        """
        Delete the object from the database.

        This method removes the object from the session, commits the changes, and logs the result.
        If an error occurs during the delete process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
            db_logger.info(f"TestCase deleted: {self.name}")
        except Exception as err:
            db_logger.error(f"Error deleting TestCase: {err}")


class TestResult(BaseSchema):
    __tablename__: str = 'test_results'
    id: Column = Column(Integer, primary_key=True)
    test_case_id: Column = Column(
        Integer, ForeignKey('test_cases.id'), nullable=False)
    test_run_id = db.Column(db.Integer, db.ForeignKey('test_run.id'))
    status: Column = Column(String(50))  # e.g., 'Passed', 'Failed', 'Error'
    execution_time: Column = Column(Float)
    failure_reason = db.Column(db.String(255))  # Time in seconds
    result_data: Column = Column(Text)
    created_at: Column = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the current object instance to a dictionary representation.

        :return: A dictionary representing the object instance.
        :rtype: Dict[str, Any]
        """
        return {
            'id': self.id,
            'test_case_id': self.test_case_id,
            'status': self.status,
            'execution_time': self.execution_time,
            'result_data': self.result_data,
            'created_at': self.created_at.isoformat()
        }

    def save(self) -> None:
        """
        Save the object to the database.

        This method adds the object to the session, commits the changes, and logs the result.
        If an error occurs during the save process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.add(self)
            db.session.commit()
            db_logger.info(f"TestResult saved: {self.test_case_id}")
        except Exception as err:
            db_logger.error(f"Error saving TestResult: {err}")

    def delete(self) -> None:
        """
        Delete the object from the database.

        This method removes the object from the session, commits the changes, and logs the result.
        If an error occurs during the delete process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
            db_logger.info(f"TestResult deleted: {self.test_case_id}")
        except Exception as err:
            db_logger.error(f"Error deleting TestResult: {err}")


class PerformanceTest(BaseSchema):
    __tablename__: str = 'performance_tests'
    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String(128), nullable=False)
    description: Column = Column(String(256))
    test_suite_id = db.Column(db.Integer, db.ForeignKey('test_suite.id'))
    config: Column = Column(Text)
    created_at: Column = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            """
        Converts the object to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary representing the object with the following keys:
                - 'id': The ID of the object.
                - 'name': The name of the object.
                - 'description': The description of the object.
                - 'config': The configuration of the object.
                - 'created_at': The creation timestamp of the object in ISO format.
        """
            'name': self.name,
            'description': self.description,
            'config': self.config,
            'created_at': self.created_at.isoformat()
        }

    def save(self) -> None:
        """
        Save the object to the database.

        This method adds the object to the session, commits the changes, and logs the result.
        If an error occurs during the save process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.add(self)
            db.session.commit()
            db_logger.info(f"PerformanceTest saved: {self.name}")
        except Exception as err:
            db_logger.error(f"Error saving PerformanceTest: {err}")

    def delete(self) -> None:
        """
        Delete the object from the database.

        This method removes the object from the session, commits the changes, and logs the result.
        If an error occurs during the delete process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
            db_logger.info(f"PerformanceTest deleted: {self.name}")
        except Exception as err:
            db_logger.error(f"Error deleting PerformanceTest: {err}")


class PerformanceTestResult(BaseSchema):
    __tablename__: str = 'performance_results'
    id: Column = Column(Integer, primary_key=True)
    performance_test_id: Column = Column(
        Integer, ForeignKey('performance_tests.id'), nullable=False)
    execution_time: Column = Column(Float)
    status: Column = Column(String(50))  # e.g., 'Passed', 'Failed', 'Error'
    avg_response_time = db.Column(db.Float)
    requests_per_sec = db.Column(db.Float)
    result_data: Column = Column(Text)
    executed_at: Column = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary containing the object's attributes.
        """
        return {
            'id': self.id,
            'performance_test_id': self.performance_test_id,
            'execution_time': self.execution_time,
            'status': self.status,
            'result_data': self.result_data,
            'executed_at': self.executed_at.isoformat()
        }

    def save(self) -> None:
        """
        Save the object to the database.

        This method adds the object to the session, commits the changes, and logs the result.
        If an error occurs during the save process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.add(self)
            db.session.commit()
            db_logger.info(
                f"PerformanceResult saved: {self.performance_test_id}")
        except Exception as err:
            db_logger.error(f"Error saving PerformanceResult: {err}")

    def delete(self) -> None:
        """
        Delete the object from the database.

        This method removes the object from the session, commits the changes, and logs the result.
        If an error occurs during the delete process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
            db_logger.info(
                f"PerformanceResult deleted: {self.performance_test_id}")
        except Exception as err:
            db_logger.error(f"Error deleting PerformanceResult: {err}")


class TestRun(BaseSchema):
    __tablename__: str = 'test_run'
    id: Column = Column(Integer, primary_key=True)
    test_suite_id: Column = Column(
        Integer, ForeignKey('test_suite.id'), nullable=False)
    created_at: Column = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary containing the object's attributes.
        """
        return {
            'id': self.id,
            'test_suite_id': self.test_suite_id,
            'created_at': self.created_at.isoformat()
        }

    def save(self) -> None:
        """
        Save the object to the database.

        This method adds the object to the session, commits the changes, and logs the result.
        If an error occurs during the save process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.add(self)
            db.session.commit()
            db_logger.info(f"TestRun saved: {self.id}")
        except Exception as err:
            db_logger.error(f"Error saving TestRun: {err}")


class User(BaseSchema):
    __tablename__: str = 'users'
    id: Column = Column(Integer, primary_key=True)
    username: Column = Column(String(128), unique=True, nullable=False)
    email: Column = Column(String(128), unique=True, nullable=False)
    password_hash: Column = Column(String(256))

    def set_password(self, password: str) -> None:
        """
        Sets the password for the user.

        Args:
            password (str): The new password for the user.

        Returns:
            None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the stored password hash.

        Args:
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches the stored password hash, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dictionary representation.

        :return: A dictionary representation of the object.
        :rtype: Dict[str, Any]
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    def save(self) -> None:
        """
        Save the object to the database.

        This method adds the object to the session, commits the changes, and logs the result.
        If an error occurs during the save process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.add(self)
            db.session.commit()
            db_logger.info(f"User saved: {self.username}")
        except Exception as err:
            db_logger.error(f"Error saving User: {err}")

    def delete(self) -> None:
        """
        Delete the object from the database.

        This method removes the object from the session, commits the changes, and logs the result.
        If an error occurs during the delete process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
            db_logger.info(f"User deleted: {self.username}")
        except Exception as err:
            db_logger.error(f"Error deleting User: {err}")


# Role Model
class Role(BaseSchema):
    __tablename__: str = 'roles'
    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String(80), unique=True)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dictionary representation.

        :return: A dictionary representing the object.
        :rtype: Dict[str, Any]
        """
        return {
            'id': self.id,
            'name': self.name
        }

    def save(self) -> None:
        """
        Save the object to the database.

        This method adds the object to the session, commits the changes, and logs the result.
        If an error occurs during the save process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.add(self)
            db.session.commit()
            db_logger.info(f"Role saved: {self.name}")

        except Exception as err:
            db_logger.error(f"Error saving Role: {err}")

    def delete(self) -> None:
        """
        Delete the object from the database.

        This method removes the object from the session, commits the changes, and logs the result.
        If an error occurs during the delete process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
            db_logger.info(f"Role deleted: {self.name}")

        except Exception as err:
            db_logger.error(f"Error deleting Role: {err}")


# AppSettings Model (if still relevant)
class AppSettings(BaseSchema):
    __tablename__: str = 'app_settings'
    id: Column = Column(Integer, primary_key=True)
    setting_name: Column = Column(String(128), unique=True, nullable=False)
    setting_value: Column = Column(String(256), nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the current object to a dictionary representation.

        :return: A dictionary containing the object's attributes.
        :rtype: Dict[str, Any]
        """
        return {
            'id': self.id,
            'setting_name': self.setting_name,
            'setting_value': self.setting_value
        }

    def save(self) -> None:
        """
        Save the object to the database.

        This method adds the object to the session, commits the changes, and logs the result.
        If an error occurs during the save process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.add(self)
            db.session.commit()
            db_logger.info(f"AppSettings saved: {self.setting_name}")

        except Exception as err:
            db_logger.error(f"Error saving AppSettings: {err}")

    def delete(self) -> None:
        """
        Delete the object from the database.

        This method removes the object from the session, commits the changes, and logs the result.
        If an error occurs during the delete process, an error message is logged.

        Parameters:
            None

        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
            db_logger.info(f"AppSettings deleted: {self.setting_name}")
        except Exception as err:
            db_logger.error(f"Error deleting AppSettings: {err}")


# One-to-many
TestSuite.test_cases = db.relationship('TestCase', lazy='dynamic', backref='test_suite')

# Many-to-one
TestCase.test_suite = db.relationship('TestSuite', back_populates="test_cases")

# One-to-many
TestRun.test_results = db.relationship('TestResult', lazy='dynamic')

# Many-to-one
TestResult.test_run = db.relationship('TestRun', back_populates="test_results")

# One-to-many
PerformanceTest.performance_results = db.relationship(
    'PerformanceResult', lazy='dynamic')

# Many-to-one
PerformanceTestResult.performance_test = db.relationship(
    'PerformanceTest', back_populates="performance_results")
