from functools import wraps, update_wrapper
from datetime import datetime, timedelta

from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restful import abort
from itsdangerous import SignatureExpired, BadSignature, TimedJSONWebSignatureSerializer as Serializer

from classes.config import config
from db import session
from models.user import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str) -> bool:
    """
    Authentication (basic auth).
    Check if username and password match. If the number of failed checks exceeds the limit, verification is
    temporarily prohibited.
    """
    user = session.query(User).filter(User.name == username).first()
    # Time blockade
    if not user or (user.blocked_since is not None and user.blocked_since > datetime.now()):
        return False
    # Check pass
    if not user.verify_password(password):
        user.failed_logins = user.failed_logins + 1
        # Check failed logins
        if user.failed_logins >= config['AUTOBLOCKADE_ATTEMPTS']:
            user.blocked_since = datetime.now() + timedelta(minutes=config['AUTOBLOCKADE_TIME'])
            user.failed_logins = 0
            # TODO: send msg to logging system
        session.add(user)
        session.commit()
        return False
    auth.user = user
    user.failed_logins = 0
    session.add(user)
    session.commit()
    return True


@auth.login_required
def get_auth_tokens():
    """
    Returns new pair of tokens for authenticated user.
    """
    return _new_auth_tokens(auth.user.id)


def refresh_token():
    """
    Check request's refresh token and return new pair of tokens.
    """
    json = request.get_json()
    token = json['refresh_token']
    data = _check_token(token, 'refresh')
    current_user = session.query(User).filter(User.id == data['id']).first()
    auth.user = current_user

    # return jsonify({'msg': 'ok'})
    return _new_auth_tokens(auth.user.id)


def generate_auth_token(user_id: int, expiration: int = config['SECRET_ACCESS_KEY_EXPIRATION']):
    """
    Return access token for given user id and expiration time.
    """
    s = Serializer(config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': user_id,
                    'grand_type': 'access'
                    })


def generate_refresh_token(user_id: int, expiration: int = config['SECRET_REFRESH_KEY_EXPIRATION']):
    """
    Return refresh token for given user id and expiration time.
    """
    s = Serializer(config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': user_id,
                    'grand_type': 'refresh'
                    })


def _new_auth_tokens(user_id: int):
    """
    Return json with new pair of access and refresh tokens for selected user id.
    """
    a_token = generate_auth_token(user_id)
    r_token = generate_refresh_token(user_id)
    return jsonify({'access_token': a_token.decode('ascii'),
                    'refresh_token': r_token.decode('ascii')
                    })


def _check_token(token, grand_type='access'):
    """
    Check and return data associated with this token.
    On error returns status code with msg.
    """
    if not token:
        abort(401, message="a valid token is missing")
    try:
        s = Serializer(config['SECRET_KEY'])
        data = s.loads(token)
    except SignatureExpired:
        abort(401, message="token expired")
    except BadSignature:
        abort(401, message="token is invalid")
    if not data['grand_type'] or data['grand_type'] != grand_type:
        abort(401, message='an {} token is missing'.format(grand_type))

    return data


# Decorators

def token_required(f):
    """
    Decorator. Checks token provided in 'x-access-tokens' header field.
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        data = _check_token(token)

        current_user = session.query(User).filter(User.id == data['id']).first()
        auth.user = current_user

        return f(*args, **kwargs)

    return decorator


class Rights:
    ADMIN = 1
    MOD = 2
    USER = 3
    BOT = 4


def access_required(min_access_rights):
    """
    Decorator. Checks whether the user has access rights to the resource.
    """

    def decorator(fn):
        @token_required
        def wrapped_function(*args, **kwargs):
            if auth.user.user_type > min_access_rights:
                abort(403, message="insufficient access rights")
            return fn(*args, **kwargs)

        return update_wrapper(wrapped_function, fn)

    return decorator
