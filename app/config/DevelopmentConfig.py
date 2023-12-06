import os

DevelopmentConfig: dict = {
    'SQLALCHEMY_DATABASE_URI': os.getenv('DEVELOPMENT_DATABASE_URI', 'sqlite:///orchestrator_dev.db'),
    'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY', 'your_jwt_secret'),
    'DEBUG': True
}
