from typing import List, Dict, Any
from influxdb import InfluxDBClient, ResultSet
from sqlalchemy.sql import count
from app.extensions import influxdb_client, db
from app.db.schema import TestResult, PerformanceTestResult
from app.utils.logger import service_logger


class PerformanceDataService:
    def __init__(self, db_session=None):
        self.db_session = db_session or db.session

    def calculate_average_response_time(self):
        """Calculate average response time from PerformanceTestResult."""
        avg_response_time = self.db_session.query(
            func.avg(PerformanceTestResult.execution_time)).scalar()
        service_logger.info("Calculated average response time")
        return avg_response_time

    def calculate_success_rate(self):
        """Calculate success rate from TestResult."""
        total_tests = self.db_session.query(count(TestResult.id)).scalar()
        successful_tests = self.db_session.query(count(TestResult.id)).filter(
            TestResult.status == 'Passed').scalar()
        success_rate = (successful_tests / total_tests) * \
            100 if total_tests else 0
        service_logger.info("Calculated success rate")
        return success_rate

    def aggregate_test_results(self):
        """Aggregate test results."""
        return {
            'average_response_time': self.calculate_average_response_time(),
            'success_rate': self.calculate_success_rate()
        }

    def save_performance_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Write performance data to the InfluxDB.

        Args:
            data (List[Dict[str, Any]]): A list of dictionaries representing the performance data.
        """
        try:
            test_id = data[0]["test_id"]
            service_logger.info(
                f"Writing performance data for test_id: {test_id}")
            performance_data = PerformanceTestResult(
                test_id=test_id, execution_time=data[0]["execution_time"])
            self.db_session.add(performance_data)
            self.db_session.commit()
            service_logger.info(
                f"Added performance data for test_id: {test_id}")
            service_logger.info(
                f"Writing performance data to InfluxDB for test_id: {test_id}")
            influxdb_client.write_points(
                [{"measurement": "performance", "tags": {"test_id": test_id}, "fields": data}])
            service_logger.info("Wrote performance data to InfluxDB")
        except Exception as err:
            service_logger.error(
                f"Error saving performance data for test_id {test_id}: {err}")

    def get_performance_data(self, query: str) -> ResultSet:
        """
        Query performance data from the InfluxDB.

        Args:
            query (str): The query string to retrieve data from InfluxDB.

        Returns:
            InfluxDBClient.ResultSet: The result set of the query.
        """
        performance_data: Dict[str, float] = {}
        try:
            performance_data = influxdb_client.query(query)
            service_logger.info(f"Retrieved performance data")
        except Exception as e:
            service_logger.error(
                f"Error retrieving performance data: {e}")

        return performance_data
