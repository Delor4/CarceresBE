from flask_restful import Resource, fields
from flask_restful import abort
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.NestedWidthEmpty import NestedWithEmpty
from classes.auth import token_required, auth
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
    @token_required
    @marshal_with(user_fields)
    def get(self, id):
        print(auth.user)
        print(auth.user.name)
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        return user

    @token_required
    def delete(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        session.delete(user)
        session.commit()
        return {}, 204

    @token_required
    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        user = session.query(User).filter(User.id == id).first()
        user.name = parsed_args['name']
        user.user_type = parsed_args['user_type']
        user.hash_password(parsed_args['password'])
        session.add(user)
        session.commit()
        return user, 201


class UserListResource(Resource):
    @token_required
    @marshal_with(user_fields)
    def get(self):
        users = session.query(User).all()
        return users

    @token_required
    @marshal_with(user_fields)
    def post(self):
        parsed_args = parser.parse_args()
        user = User(name=parsed_args['name'], user_type=parsed_args['user_type'], )
        user.hash_password(parsed_args['password'])
        session.add(user)
        session.commit()
        return user, 201
