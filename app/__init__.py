from typing import Literal
from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.api import api_blueprint

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orchestrator.db'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config.from_envvar('APP_SETTINGS')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.errorhandler(Exception)
    def handle_exception(error) -> tuple[Response, Literal[500]]:
        response = {"error": str(error)}
        return jsonify(response), 500

    @app.errorhandler(404)
    def resource_not_found(e) -> tuple[Response, Literal[404]]:
        return jsonify(error=str(e)), 404

    return app
