from typing import Any
from app.db import db
from datetime import datetime


class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    test_cases = db.relationship('TestCase', backref='test_suite', lazy=True)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "test_cases": self.test_cases
        }
    

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_suite_id = db.Column(db.Integer, db.ForeignKey(
        'test_suite.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "test_suite_id": self.test_suite_id
        }


class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey(
        'test_case.id'), nullable=False)
    status = db.Column(db.String(50))  # e.g., 'Passed', 'Failed', 'Error'
    execution_time = db.Column(db.Float)  # Time in seconds
    # JSON string or plain text with result details
    result_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'test_case_id': self.test_case_id,
            'status': self.status,
            'execution_time': self.execution_time,
            'result_data': self.result_data,
            'created_at': self.created_at.isoformat()
        }

class PerformanceTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    config = db.Column(db.Text)  # JSON or YAML string with test configuration
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    results = db.relationship('PerformanceResult', backref='performance_test', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'config': self.config,
            'created_at': self.created_at.isoformat()
        }
    
class PerformanceResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    performance_test_id = db.Column(db.Integer, db.ForeignKey('performance_test.id'), nullable=False)
    execution_time = db.Column(db.Float)  # Time in seconds
    status = db.Column(db.String(50))  # e.g., 'Passed', 'Failed', 'Error'
    result_data = db.Column(db.Text)  # JSON string with detailed result data
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'performance_test_id': self.performance_test_id,
            'execution_time': self.execution_time,
            'status': self.status,
            'result_data': self.result_data,
            'executed_at': self.executed_at.isoformat()
        }
