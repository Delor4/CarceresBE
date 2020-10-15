from functools import wraps, update_wrapper

from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restful import abort
from itsdangerous import SignatureExpired, BadSignature, TimedJSONWebSignatureSerializer as Serializer

from classes.config import config
from db import session
from models.user import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter(User.name == username).first()
    if not user or not user.verify_password(password):
        return False
    auth.user = user
    return True


def generate_auth_token(user_id, expiration=config['SECRET_KEY_EXPIRATION']):
    s = Serializer(config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': user_id})


@auth.login_required
def get_auth_token():
    token = generate_auth_token(auth.user.id)
    return jsonify({'token': token.decode('ascii')})


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            abort(401, message="a valid token is missing")

        try:
            s = Serializer(config['SECRET_KEY'])
            data = s.loads(token)
        except SignatureExpired:
            abort(401, message="token expired")
        except BadSignature:
            abort(401, message="token is invalid")

        current_user = session.query(User).filter(User.id == data['id']).first()
        auth.user = current_user

        return f(*args, **kwargs)

    return decorator


def access_required(min_access_rights):
    def decorator(fn):
        @token_required
        def wrapped_function(*args, **kwargs):
            if auth.user.user_type > min_access_rights:
                abort(403, message="insufficient access rights")
            return fn(*args, **kwargs)

        return update_wrapper(wrapped_function, fn)

    return decorator
