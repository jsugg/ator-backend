from flask import Flask
from app import create_app
from app.utils.logger import app_logger

environment: str = 'development'
app: Flask = create_app(environment)

if __name__ == '__main__':
    app_logger.info(f"Starting application in {environment} mode")
    app.run(debug=True)
