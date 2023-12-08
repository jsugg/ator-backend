from typing import Dict, Any, List
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime

# TestSuite Model
class TestSuite(db.Model):
    __tablename__ = 'test_suites'

    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String(128), nullable=False)
    description: Column = Column(String(256), nullable=True)
    test_cases: relationship = relationship('TestCase', backref='test_suite', lazy='dynamic')

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

# TestCase Model
class TestCase(db.Model):
    __tablename__ = 'test_cases'

    id: Column = Column(Integer, primary_key=True)
    test_suite_id: Column = Column(Integer, ForeignKey('test_suites.id'), nullable=False)
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

# TestResult Model
class TestResult(db.Model):
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
        return {
            'id': self.id,
            'test_case_id': self.test_case_id,
            'status': self.status,
            'execution_time': self.execution_time,
            'result_data': self.result_data,
            'created_at': self.created_at.isoformat()
        }

# PerformanceTest Model
class PerformanceTest(db.Model):
    __tablename__: str = 'performance_tests'
    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String(128), nullable=False)
    description: Column = Column(String(256))
    test_suite_id = db.Column(db.Integer, db.ForeignKey('test_suite.id'))
    config: Column = Column(Text)
    created_at: Column = Column(DateTime, default=datetime.utcnow)
    results: relationship = relationship(
        'PerformanceResult', backref='performance_test', lazy='dynamic')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'config': self.config,
            'created_at': self.created_at.isoformat()
        }

# PerformanceResult Model
class PerformanceResult(db.Model):
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
        return {
            'id': self.id,
            'performance_test_id': self.performance_test_id,
            'execution_time': self.execution_time,
            'status': self.status,
            'result_data': self.result_data,
            'executed_at': self.executed_at.isoformat()
        }

# User Model
class User(db.Model):
    __tablename__: str = 'users'
    id: Column = Column(Integer, primary_key=True)
    username: Column = Column(String(128), unique=True, nullable=False)
    email: Column = Column(String(128), unique=True, nullable=False)
    password_hash: Column = Column(String(256))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

# Role Model
class Role(db.Model):
    __tablename__: str = 'roles'
    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String(80), unique=True)

# AppSettings Model (if still relevant)
class AppSettings(db.Model):
    __tablename__: str = 'app_settings'
    id: Column = Column(Integer, primary_key=True)
    setting_name: Column = Column(String(128), unique=True, nullable=False)
    setting_value: Column = Column(String(256), nullable=False)






# One-to-many
TestSuite.test_cases = db.relationship('TestCase', lazy='dynamic')  

# Many-to-one
TestCase.test_suite = db.relationship('TestSuite', back_populates="test_cases")

# One-to-many 
TestRun.test_results = db.relationship('TestResult', lazy='dynamic')

# Many-to-one
TestResult.test_run = db.relationship('TestRun', back_populates="test_results")

# One-to-many
PerformanceTest.performance_results = db.relationship('PerformanceResult', lazy='dynamic')
 
# Many-to-one 
PerformanceResult.performance_test = db.relationship('PerformanceTest', back_populates="performance_results")