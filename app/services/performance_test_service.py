import os
import csv
import subprocess
import threading
import signal
import time
from typing import Any, Dict, List, Optional
from flask import current_app
from app.schemas.performance_test import PerformanceTest
from app.schemas.test_run import TestRun
from sqlalchemy.orm import Session
from datetime import datetime


class LocustPerformanceTester:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def execute_test(self, performance_test_id: int = None, test_run_id: str = None) -> Dict[str, Any]:
        test = self._get_test(performance_test_id)
        if not test:
            return {"status": "Error", "message": "Test not found"}

        test_run = self._get_or_create_test_run(test_run_id)
        test_run.statuses[performance_test_id] = "started"
        self.db_session.commit()

        try:
            locust_command = self._build_locust_command(test.config)
            result_file_prefix = f"locust_result_{performance_test_id}"
            process = subprocess.Popen(locust_command, shell=True)

            # Save process ID to file for later termination
            with open(f"locust_{performance_test_id}.pid", "w") as f:
                f.write(str(process.pid))

            # Wait for process to finish
            process.wait()

            # Parse and aggregate test results
            results = self._parse_locust_test_results(
                f"{result_file_prefix}.csv")
            aggregated_data = self._aggregate_test_results(results)

            # Update test run status and save results
            test_run.statuses[performance_test_id] = "completed"
            test_run.results = aggregated_data
            self.db_session.commit()

            # Cleanup test resources
            self._cleanup_test_resources(result_file_prefix)
            os.remove(f"locust_{performance_test_id}.pid")

            return {"status": "completed", "test_id": performance_test_id, "test_run_id": test_run_id, "results": aggregated_data}
        except Exception as e:  # Catching a broad exception to handle any subprocess-related errors
            current_app.logger.error(f"Locust test execution failed: {e}")
            test_run.statuses[performance_test_id] = "error"
            self.db_session.commit()
            return {"status": "Error", "message": str(e)}

    def execute_test_async(self, performance_test_id: int, test_run_id: str) -> None:
        threading.Thread(target=self.execute_test, args=(
            performance_test_id, test_run_id)).start()

    def stop_performance_test(self, test_id: int, test_run_id: str) -> None:
        test_run = self.db_session.query(
            TestRun).filter_by(id=test_run_id).first()
        if not test_run:
            print(f"No test run found with ID {test_run_id}")
            return

        if test_id not in test_run.statuses:
            print(f"Test ID {test_id} not found in test run {test_run_id}")
            return

        # Get Locust process ID from saved PID file
        pid_file = f"locust_{test_id}.pid"
        try:
            with open(pid_file) as f:
                locust_pid = int(f.read())
        except IOError:
            print(f"Could not read PID file {pid_file}")
            return

        # Send SIGTERM signal to terminate Locust process
        try:
            os.kill(locust_pid, signal.SIGTERM)
            print(f"Sent termination signal to Locust process {locust_pid}")
        except ProcessLookupError:
            print(f"Process {locust_pid} not found")

        # Allow time for process to terminate
        time.sleep(5)

        # Cleanup test resources
        self._cleanup_test_resources(f"locust_result_{test_id}")
        self._cleanup_test_resources(pid_file)

        test_run.statuses[test_id] = 'stopped'
        self.db_session.commit()

    def schedule_test_execution(self, test_id: int, test_run_id: str, delay: int) -> None:
        def delayed_execution() -> None:
            time.sleep(delay)
            self.execute_test(test_id, test_run_id)

        threading.Thread(target=delayed_execution).start()

    def get_test_status_by_run_id(self, test_run_id: str) -> TestRun:
        return self.db_session.query(TestRun).filter_by(id=test_run_id).first()

    @staticmethod
    def _build_locust_command(config: Dict[str, Any]) -> str:
        return (f"locust -f {config.get('locustfile')} --headless "
                f"--users {config.get('users', 10)} --spawn-rate {config.get('spawn_rate', 1)} "
                f"--run-time {config.get('run_time', '1m')} --host {config.get('host')} "
                f"--csv={config.get('result_file_prefix', 'locust_result')}")

    @staticmethod
    def _parse_locust_test_results(csv_file: str) -> List[Dict[str, Any]]:
        try:
            with open(csv_file, mode='r') as file:
                csv_reader = csv.DictReader(file)
                return [row for row in csv_reader]
        except IOError as e:
            current_app.logger.error(f"Error reading Locust result file: {e}")
            return []

    @staticmethod
    def _get_test(test_id: int) -> Optional[PerformanceTest]:
        return PerformanceTest.query.get(test_id)

    def _get_or_create_test_run(self, test_run_id: str) -> TestRun:
        test_run = self.db_session.query(
            TestRun).filter_by(id=test_run_id).first()
        if not test_run:
            test_run = TestRun(id=test_run_id, statuses={},
                               created_at=datetime.now(), updated_at=datetime.now())
            self.db_session.add(test_run)
            self.db_session.commit()
        return test_run

    def _cleanup_test_resources(self, resource_prefix: str) -> None:
        for filename in os.listdir('.'):
            if filename.startswith(resource_prefix):
                os.remove(filename)

    def _aggregate_test_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregates and analyzes the test results.

        :param results: List of test result data
        :return: Aggregated result data
        """
        aggregated_data = {}
        for result in results:
            # Process each result and update aggregated_data
            # Example: aggregated_data['some_metric'] = calculate_metric(result)
            pass

        return aggregated_data
