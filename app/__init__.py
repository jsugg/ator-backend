from typing import Literal
from flask import Flask, Response, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.api import api_blueprint
from app.db import db


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

    @app.errorhandler(405)
    def method_not_allowed(e) -> tuple[Response, Literal[405]]:
        return jsonify(error=str(e)), 405

    @app.errorhandler(400)
    def bad_request(e) -> tuple[Response, Literal[400]]:
        return jsonify(error=str(e)), 400
    
    @app.errorhandler(401)
    def unauthorized(e) -> tuple[Response, Literal[401]]:
        return jsonify(error=str(e)), 401
    
    @app.errorhandler(403)
    def forbidden(e) -> tuple[Response, Literal[403]]:
        return jsonify(error=str(e)), 403

    @app.errorhandler(404)
    def resource_not_found(e) -> tuple[Response, Literal[404]]:
        return jsonify(error=str(e)), 404

    return app
