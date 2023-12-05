from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orchestrator.db'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.errorhandler(Exception)
    def handle_exception(error):
        # Handle specific exceptions or general exception
        response = {"error": str(error)}
        return jsonify(response), 500

    return app

# In app/__init__.py
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500
