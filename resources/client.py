from flask_restful import Resource
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.NestedWidthEmpty import NestedWithEmpty
from classes.auth import access_required
from db import session
from models.client import Client
from models.user import User
from resources.car import car_fields

client_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'surname': fields.String,
    'address': fields.String,
    'city': fields.String,
    'phone': fields.String,
    'cars': fields.Nested(car_fields),
    'user_id': fields.Integer,
    'user': NestedWithEmpty({
        'id': fields.Integer,
        'name': fields.String,
        'user_type': fields.Integer,
        'uri': fields.Url('user', absolute=True),
    }, allow_null=True),
    'uri': fields.Url('client', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('surname', type=str, required=True, nullable=False)
parser.add_argument('address', type=str, required=False, nullable=True)
parser.add_argument('city', type=str, required=False, nullable=True)
parser.add_argument('phone', type=str, required=False, nullable=True)
parser.add_argument('user_id', type=int, required=False, nullable=True)


class ClientResource(Resource):
    @access_required(2)
    @marshal_with(client_fields)
    def get(self, id):
        client = session.query(Client).filter(Client.id == id).first()
        if not client:
            abort(404, message="Client {} doesn't exist".format(id))
        return client

    @access_required(2)
    def delete(self, id):
        client = session.query(Client).filter(Client.id == id).first()
        if not client:
            abort(404, message="Client {} doesn't exist".format(id))
        session.delete(client)
        session.commit()
        return {}, 204

    @access_required(2)
    @marshal_with(client_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        client = session.query(Client).filter(Client.id == id).first()
        client.name = parsed_args['name']
        client.surname = parsed_args['surname']
        client.address = parsed_args['address']
        client.city = parsed_args['city']
        client.phone = parsed_args['phone'],
        client.user_id = parsed_args['user_id']
        user = session.query(User).filter(User.id == parsed_args['user_id']).first()
        if user is not None:
            user.client = client
            client.user.append(user)
        session.add(client)
        session.commit()
        return client, 201


class ClientListResource(Resource):
    @access_required(2)
    @marshal_with(client_fields)
    def get(self):
        clients = session.query(Client).all()
        return clients

    @access_required(2)
    @marshal_with(client_fields)
    def post(self):
        parsed_args = parser.parse_args()
        client = Client(name=parsed_args['name'],
                        surname=parsed_args['surname'],
                        address=parsed_args['address'],
                        city=parsed_args['city'],
                        phone=parsed_args['phone'],
                        user_id=parsed_args['user_id'],
                        )
        user = session.query(User).filter(User.id == parsed_args['user_id']).first()
        if user is not None:
            user.client = client
            client.user = user
        session.add(client)
        session.commit()
        return client, 201
