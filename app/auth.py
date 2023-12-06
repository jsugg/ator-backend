from flask import Blueprint, Response, request, url_for
from flask_oauthlib.client import OAuth

auth_blueprint = Blueprint('auth_blueprint', __name__)
oauth = OAuth()

keycloak = oauth.remote_app(
    'keycloak',
    consumer_key='KEYCLOAK_CLIENT_ID',
    consumer_secret='KEYCLOAK_CLIENT_SECRET',
    request_token_params={'scope': 'openid'},
    base_url='KEYCLOAK_URL',
    access_token_url='/realms/KEYCLOAK_REALM/protocol/openid-connect/token',
    authorize_url='/realms/KEYCLOAK_REALM/protocol/openid-connect/auth',
)


@auth_blueprint.route('/login')
def login() -> Response:
    return keycloak.authorize(callback=url_for('auth_blueprint.authorized', _external=True))


@auth_blueprint.route('/logout')
def logout() -> None:
    # TODO: Implement logout functionality
    pass


@auth_blueprint.route('/login/authorized')
def authorized() -> str:
    resp = keycloak.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return f"Access denied: reason={request.args['error_reason']} error={request.args['error_description']}"
    # TODO: Store the access_token in a Redisdatabase. Use the access_token in resp to authenticate users
    return 'Logged in successfully.'
