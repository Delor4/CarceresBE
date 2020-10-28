from flask import url_for
from flask_restful import Resource, fields
from flask_restful import abort
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.NestedWidthEmpty import NestedWithEmpty
from classes.auth import token_required, access_required, Rights
from classes.views import list_view, make_response_headers
from db import session
from models.user import User

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'user_type': fields.Integer,
    'uri': fields.Url('user', absolute=True),
    'password_hash': fields.String,
    'client': NestedWithEmpty({
        'id': fields.Integer,
        'name': fields.String,
        'surname': fields.String,
        'address': fields.String,
        'city': fields.String,
        'phone': fields.String,
        'user_id': fields.Integer,
        'uri': fields.Url('client', absolute=True),
    }, allow_null=True),
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('user_type', type=str)
parser.add_argument('password', type=str, required=True, nullable=False)


class UserResource(Resource):
    """
    Resources for 'user' (/api/users/<id>) endpoint.
    """

    @access_required(Rights.MOD)
    @marshal_with(user_fields)
    def get(self, id):
        """
        Returns user's data.
        """
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        return user, 200, make_response_headers(user)

    @access_required(Rights.ADMIN)
    def delete(self, id):
        """
        Delete user from database.
        """
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        session.delete(user)
        session.commit()
        return {}, 204

    @access_required(Rights.ADMIN)
    @marshal_with(user_fields)
    def put(self, id):
        """
        Update user's data.
        """
        parsed_args = parser.parse_args()
        user = session.query(User).filter(User.id == id).first()
        user.name = parsed_args['name']
        user.user_type = parsed_args['user_type']
        user.hash_password(parsed_args['password'])
        session.add(user)
        session.commit()
        return user, 201, make_response_headers(user)


class UserListResource(Resource):
    """
    Resources for 'users' (/api/users) endpoint.
    """

    @token_required
    def get(self):
        """
        Returns data of all users.
        """
        return list_view(User, user_fields, url_for(self.endpoint, _external=True))

    @access_required(Rights.ADMIN)
    @marshal_with(user_fields)
    def post(self):
        """
        Create new user.
        """
        parsed_args = parser.parse_args()
        user = User(name=parsed_args['name'], user_type=parsed_args['user_type'], )
        user.hash_password(parsed_args['password'])
        session.add(user)
        session.commit()
        return user, 201, make_response_headers(user, location=url_for('user', id=user.id, _external=True))
