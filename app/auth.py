from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from functools import wraps
from sqlalchemy.exc import IntegrityError

from responses import error_response, token_response, success_response
from model.user import User
from model.common import db

MISSING_JSON = "Missing JSON"
MISSING_PARAMETER = "Missing Username or Password"
INVALID_LOGIN = "Invalid login"
DUPLICATE_USER = "Username is already registered"

USER_CREATED = "User created"


auth = Blueprint('auth', __name__)


def require_json(func):
    @wraps(func)
    def wrapper():
        if not request.is_json:
            return error_response(MISSING_JSON)
        return func()
    return wrapper


# Pass username and password in cleartext
# Only for demonstration purpose
# In them future change to more secure method
@auth.route('/register', methods=['POST'])
@require_json
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    print(username, password)
    if not username or not password:
        return error_response(MISSING_PARAMETER)
    user = User(username=username, password=password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return error_response(DUPLICATE_USER)
    return success_response(USER_CREATED)


@auth.route('/login', methods=['POST'])
@require_json
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return error_response(MISSING_PARAMETER)

    # Auth here
    user = User.query.filter_by(username=username).first()
    if user.password != password:
        return error_response(INVALID_LOGIN, 401)

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=user.id)
    return token_response(access_token)
