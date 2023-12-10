from typing import Any, Literal
from flask_restx import Namespace, Resource, fields
from flask import jsonify, request, session, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from app.extensions import keycloak
from app.config import Config
from urllib.parse import urlencode
from app.utils.logger import auth_logger

auth_ns = Namespace('Auth', description='Authentication related operations')

login_model = auth_ns.model('LoginModel', {
    'callback_url': fields.String(required=True, description='Callback URL for authentication')
})

login_response_model = auth_ns.model('LoginResponse', {
    'message': fields.String(description='Response message after successful login')
})

logout_response_model = auth_ns.model('LogoutResponse', {
    'message': fields.String(description='Response message after successful logout')
})

user_info_model = auth_ns.model('UserInfo', {
    'current_user': fields.String(description='Identifier of the current user'),
    'keycloak_user_info': fields.Raw(description='User information from Keycloak')
})

error_model = auth_ns.model('ErrorResponse', {
    'error': fields.String(description='Error message')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('login')
    @auth_ns.response(302, 'Redirect to authentication page', login_response_model)
    @auth_ns.response(401, 'Unauthorized', error_model)
    def get(self) -> Any | tuple[dict[str, str], Literal[500]]:
            """User login endpoint. Redirects to Keycloak login page."""
            try:
                callback_url = url_for('.authorized', _external=True)
                response = keycloak.authorize(callback=callback_url)
                auth_logger.info("User login attempted.")
                return response
            except Exception as e:
                auth_logger.error(f"Login failed: {str(e)}")
                return {'message': 'Internal server error'}, 500



@auth_ns.route('/login/authorized')
class Authorized(Resource):
    @auth_ns.doc('authorized')
    @auth_ns.response(200, 'Login successful', login_response_model)
    @auth_ns.response(401, 'Unauthorized', error_model)
    def get(self):
        """Callback endpoint for processing login. Returns login status."""
        try:
            response = keycloak.authorized_response()
            if response is None or 'access_token' not in response:
                auth_logger.warning("Unauthorized access attempt or login failed.")
                return jsonify({'error': 'Access denied or login failed'}), 401
            session['keycloak_token'] = (response['access_token'], '')
            auth_logger.info("Login successful.")
            return jsonify({'message': 'Logged in successfully'})
        except Exception as e:
            auth_logger.error(f"Login authorized error: {str(e)}")
            return {'message': 'Internal server error'}, 500



@auth_ns.route('/logout')
class Logout(Resource):
    @auth_ns.doc('logout')
    @auth_ns.response(200, 'Logout successful', logout_response_model)
    @jwt_required()
    def post(self):
        """User logout endpoint. Logs out the current user."""
        try:
            session.pop('keycloak_token', None)
            auth_logger.info("User logged out successfully.")
            return jsonify({'message': 'Logged out successfully'})
        except Exception as e:
            auth_logger.error(f"Logout error: {str(e)}")
            return {'message': 'Internal server error'}, 500



@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.doc('register')
    @auth_ns.response(302, 'Redirect to registration page')
    def get(self):
        """User registration endpoint. Redirects to Keycloak registration page."""
        try:
            keycloak_register_url = f"{keycloak.base_url}/realms/{Config.KEYCLOAK_REALM}/protocol/openid-connect/registrations"
            query_params = urlencode({
                'client_id': keycloak.consumer_key,
                'response_type': 'code',
                'scope': 'openid',
                'redirect_uri': url_for('.authorized', _external=True)
            })
            auth_logger.info("Redirecting to Keycloak registration page.")
            return redirect(f"{keycloak_register_url}?{query_params}")
        except Exception as e:
            auth_logger.error(f"Registration error: {str(e)}")
            return {'message': 'Internal server error'}, 500



@auth_ns.route('/user')
class CurrentUser(Resource):
    @auth_ns.doc('get_current_user')
    @auth_ns.response(200, 'User information retrieved', user_info_model)
    @auth_ns.response(401, 'Unauthorized', error_model)
    @jwt_required()
    
    def get(self):
        """Endpoint to get current user information."""
        try:
            current_user_identity = get_jwt_identity()
            keycloak_token = get_keycloak_oauth_token()
            if keycloak_token:
                headers = {'Authorization': f'Bearer {keycloak_token[0]}'}
                keycloak_user_info = keycloak.get('userinfo', headers=headers).data
                auth_logger.info(f"Retrieved user information for {current_user_identity}.")
                return jsonify({
                    'current_user': current_user_identity,
                    'keycloak_user_info': keycloak_user_info
                }), 200
            auth_logger.error("Failed to fetch user info from Keycloak.")
            return jsonify({'error': 'Unable to fetch user info from Keycloak'}), 401
        except Exception as e:
            auth_logger.error(f"User info retrieval error: {str(e)}")
            return {'message': 'Internal server error'}, 500

