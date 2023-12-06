import os

ProductionConfig: dict = {
    'SQLALCHEMY_DATABASE_URI': os.getenv('PRODUCTION_DATABASE_URI', 'postgresql://user:password@localhost/prod_db'),
    'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY', 'your_jwt_secret'),
    'DEBUG': False
}
