from typing import List, Dict, Any
from app.extensions import influxdb_client, db
from influxdb import InfluxDBClient
from sqlalchemy import func
from app.db.models import TestResult, PerformanceResult

class PerformanceDataService:
    def __init__(self, db_session=None):
        self.db_session = db_session or db.session

    def calculate_average_response_time(self):
        """Calculate average response time from PerformanceResult."""
        avg_response_time = self.db_session.query(func.avg(PerformanceResult.execution_time)).scalar()
        return avg_response_time

    def calculate_success_rate(self):
        """Calculate success rate from TestResult."""
        total_tests = self.db_session.query(func.count(TestResult.id)).scalar()
        successful_tests = self.db_session.query(func.count(TestResult.id)).filter(TestResult.status == 'Passed').scalar()
        success_rate = (successful_tests / total_tests) * 100 if total_tests else 0
        return success_rate

    def aggregate_test_results(self):
        """Aggregate test results."""
        return {
            'average_response_time': self.calculate_average_response_time(),
            'success_rate': self.calculate_success_rate()
        }

    def write_performance_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Write performance data to the InfluxDB.

        Args:
            data (List[Dict[str, Any]]): A list of dictionaries representing the performance data.
        """
        influxdb_client.write_points(data)

    def query_performance_data(self, query: str) -> InfluxDBClient.ResultSet:
        """
        Query performance data from the InfluxDB.

        Args:
            query (str): The query string to retrieve data from InfluxDB.

        Returns:
            InfluxDBClient.ResultSet: The result set of the query.
        """
        return influxdb_client.query(query)