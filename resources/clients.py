from flask_restful import fields, abort
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.ListResource import ListResource
from classes.NestedWidthEmpty import NestedWithEmpty
from classes.SingleResource import SingleResource
from classes.auth import access_required, Rights
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
        'brand': fields.String,
        'client_id': fields.Integer,
        'uri': fields.Url('car', absolute=True),
    }),
    'user_id': fields.Integer,
    'user': NestedWithEmpty({
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
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


class ClientResource(SingleResource):
    """
    Resources for 'client' (/api/clients/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Client
        self.model_name = "client"
        self.marshal_fields = client_fields

    @access_required(Rights.MOD)
    @marshal_with(client_fields)
    def get(self, id):
        """
        Returns client's data.
        """
        return self.process_get_req(id)

    @access_required(Rights.MOD)
    def delete(self, id):
        """
        Delete client from database.
        """
        return self.process_delete_req(id)

    @access_required(Rights.MOD)
    @marshal_with(client_fields)
    def put(self, id):
        """
        Update client's data.
        """
        parsed_args = parser.parse_args()
        client = self.get_model(id)

        if not parsed_args['name']:
            abort(400, message="Name not provided.")
        client.name = parsed_args['name']

        if not parsed_args['surname']:
            abort(400, message="Surname not provided.")
        client.surname = parsed_args['surname']

        client.address = parsed_args['address']
        client.city = parsed_args['city']
        client.phone = parsed_args['phone']

        client.user_id = parsed_args['user_id']
        user = session.query(User).filter(User.id == parsed_args['user_id']).first()
        if user is not None:
            user.client = client
            client.user = user
        return self.finalize_put_req(client)


class ClientListResource(ListResource):
    """
    Resources for 'clients' (/api/clients/<id>) endpoint.
    """
    def __init__(self):
        super().__init__()
        self.model_class = Client
        self.model_name = "client"
        self.marshal_fields = client_fields

    @access_required(Rights.MOD)
    def get(self):
        """
        Returns data of all clients.
        """
        return self.process_get_req()

    @access_required(Rights.MOD)
    @marshal_with(client_fields)
    def post(self):
        """
        Create new client.
        """
        parsed_args = parser.parse_args()
        if not parsed_args['name']:
            abort(400, message="Name not provided.")
        if not parsed_args['surname']:
            abort(400, message="Surname not provided.")

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
        return self.finalize_post_req(client)
