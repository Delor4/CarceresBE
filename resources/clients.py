from flask import url_for
from flask_restful import Resource
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.NestedWidthEmpty import NestedWithEmpty
from classes.auth import access_required, Rights
from classes.views import list_view
from db import session
from models.client import Client
from models.user import User

client_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'surname': fields.String,
    'address': fields.String,
    'city': fields.String,
    'phone': fields.String,
    'cars': fields.Nested({
        'id': fields.Integer,
        'plate': fields.String,
        'client_id': fields.Integer,
        'uri': fields.Url('car', absolute=True),
    }),
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
    """
    Resources for 'client' (/api/clients/<id>) endpoint.
    """

    @access_required(Rights.MOD)
    @marshal_with(client_fields)
    def get(self, id):
        """
        Returns client's data.
        """
        client = session.query(Client).filter(Client.id == id).first()
        if not client:
            abort(404, message="Client {} doesn't exist".format(id))
        return client

    @access_required(Rights.MOD)
    def delete(self, id):
        """
        Delete client from database.
        """
        client = session.query(Client).filter(Client.id == id).first()
        if not client:
            abort(404, message="Client {} doesn't exist".format(id))
        session.delete(client)
        session.commit()
        return {}, 204

    @access_required(Rights.MOD)
    @marshal_with(client_fields)
    def put(self, id):
        """
        Update client's data.
        """
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
    """
    Resources for 'clients' (/api/clients/<id>) endpoint.
    """

    @access_required(Rights.MOD)
    def get(self):
        """
        Returns data of all clients.
        """
        return list_view(Client, client_fields, url_for(self.endpoint, _external=True))

    @access_required(Rights.MOD)
    @marshal_with(client_fields)
    def post(self):
        """
        Create new client.
        """
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
