from flask import Blueprint, jsonify, session, request
from app.models import User, db
from app.forms import LoginForm
from app.forms import SignUpForm
from .aws_helpers import *
from flask_login import current_user, login_user, logout_user, login_required
import requests
from flask import abort, redirect
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from tempfile import NamedTemporaryFile
import json

auth_routes = Blueprint('auth', __name__)
"""
OATH
"""
# Import our credentials from the .env file
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
BASE_URL = os.getenv('BASE_URL')
REACT_APP_BASE_URL = os.getenv('REACT_APP_BASE_URL')

client_secrets = {
  "web": {
    "client_id": CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": CLIENT_SECRET,
    "redirect_uris": [
      f"{BASE_URL}/api/auth/callback"
    ]
  }
}

# generating a temporary file as the google oauth package requires a file for configuration
secrets = NamedTemporaryFile()
# Note that the property '.name' is the file PATH to our temporary file!
# The command below will write our dictionary to the temp file AS json!
with open(secrets.name, "w") as output:
    json.dump(client_secrets, output)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

flow = Flow.from_client_secrets_file(
    client_secrets_file=secrets.name,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri=f"{BASE_URL}/api/auth/callback"
)

secrets.close() # deletes our temporary file from the /tmp folder - We no longer need it as our flow object has been configured!

auth_routes = Blueprint('auth', __name__)

""""""



def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages


@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_dict_self()
    return {'errors': ['Unauthorized']}


@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    # Get the csrf_token from the request cookie and put it into the
    # form manually to validate_on_submit can be used
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        # Add the user to the session, we are logged in!
        user = User.query.filter(User.email == form.data['email']).first()
        login_user(user)
        return user.to_dict_self()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {'message': 'User logged out'}


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        image = form.data['profile_img']
        image.filename = get_unique_filename(image.filename)
        upload = upload_file_to_s3(image)
        user = User(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password'],
            first_name = form.data['first_name'].title(),
            last_name = form.data["last_name"].title(),
            address = form.data['address'],
            city = form.data['city'].title(),
            state = form.data['state'],
            profile_img = upload['url'],
            description = form.data['description']
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return user.to_dict_self()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': ['Unauthorized']}, 401

@auth_routes.route('/google/key')
def get_key():
    return {'key': os.environ.get('REACT_APP_GOOGLE_MAPS_API_KEY')}
