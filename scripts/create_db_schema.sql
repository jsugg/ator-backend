CREATE DATABASE IF NOT EXISTS dev.db;

USE your_database_name;

CREATE TABLE IF NOT EXISTS test_suites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS test_cases (
    id INT PRIMARY KEY AUTO_INCREMENT,
    test_suite_id INT NOT NULL,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(256),
    FOREIGN KEY (test_suite_id) REFERENCES test_suites (id)
);

CREATE TABLE IF NOT EXISTS test_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    test_case_id INT NOT NULL,
    test_run_id INT,
    status VARCHAR(50),
    execution_time FLOAT,
    failure_reason VARCHAR(255),
    result_data TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_case_id) REFERENCES test_cases (id),
    FOREIGN KEY (test_run_id) REFERENCES test_run (id)
);

CREATE TABLE IF NOT EXISTS performance_tests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(256),
    test_suite_id INT,
    config TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_suite_id) REFERENCES test_suites (id)
);

CREATE TABLE IF NOT EXISTS performance_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    performance_test_id INT NOT NULL,
    execution_time FLOAT,
    status VARCHAR(50),
    avg_response_time FLOAT,
    requests_per_sec FLOAT,
    result_data TEXT,
    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (performance_test_id) REFERENCES performance_tests (id)
);

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL,
    password_hash VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(80) UNIQUE
);

CREATE TABLE IF NOT EXISTS app_settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    setting_name VARCHAR(128) UNIQUE NOT NULL,
    setting_value VARCHAR(256) NOT NULL
);

ALTER TABLE test_cases
ADD CONSTRAINT fk_test_suite
FOREIGN KEY (test_suite_id)
REFERENCES test_suites(id);

ALTER TABLE test_results
ADD CONSTRAINT fk_test_case
FOREIGN KEY (test_case_id)
REFERENCES test_cases(id);

ALTER TABLE test_results
ADD CONSTRAINT fk_test_run
FOREIGN KEY (test_run_id)
REFERENCES test_run(id);

ALTER TABLE performance_tests
ADD CONSTRAINT fk_test_suite_perf
FOREIGN KEY (test_suite_id)
REFERENCES test_suites(id);

ALTER TABLE performance_results
ADD CONSTRAINT fk_perf_test
FOREIGN KEY (performance_test_id)
REFERENCES performance_tests(id);