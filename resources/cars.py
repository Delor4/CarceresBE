from flask import url_for
from flask_restful import Resource
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.ResourceBase import ResourceBase
from classes.SingleResource import SingleResource
from classes.auth import access_required, Rights, nocache
from classes.views import list_view
from db import session
from models.car import Car
from models.client import Client

car_fields = {
    'id': fields.Integer,
    'plate': fields.String,
    'client_id': fields.Integer,
    'uri': fields.Url('car', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('plate', type=str, required=True, nullable=False)
parser.add_argument('client_id', type=int, required=True, nullable=False)


class CarResource(SingleResource):
    """
    Resources for 'car' (/api/cars/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Car
        self.model_name = "Car"
        self.marshal_fields = car_fields

    @access_required(Rights.MOD)
    @marshal_with(car_fields)
    def get(self, id):
        """
        Returns car's data.
        """
        return self.process_get_req(id)

    @access_required(Rights.MOD)
    def delete(self, id):
        """
        Delete car from database.
        """
        return self.process_delete_req(id)

    @access_required(Rights.MOD)
    @marshal_with(car_fields)
    def put(self, id):
        """
        Update car's data.
        """
        parsed_args = parser.parse_args()
        car = self.get_model(id)
        car.plate = parsed_args['plate']
        car.client_id = parsed_args['client_id']
        client = session.query(Client).filter(Client.id == parsed_args['client_id']).first()
        if not client:
            abort(404, message=f"Client {parsed_args['client_id']} doesn't exist")
        client.cars.append(car)
        return self.finalize_put_req(car)


class CarListResource(ResourceBase):
    """
    Resources for 'cars' (/api/cars) endpoint.
    """

    @access_required(Rights.MOD)
    def get(self):
        """
        Returns data of all cars.
        """
        return list_view(Car, car_fields, url_for(self.endpoint, _external=True))

    @access_required(Rights.MOD)
    @nocache
    @marshal_with(car_fields)
    def post(self):
        """
        Create new car.
        """
        parsed_args = parser.parse_args()
        car = Car(plate=parsed_args['plate'], client_id=parsed_args['client_id'])
        client = session.query(Client).filter(Client.id == parsed_args['client_id']).first()
        client.cars.append(car)
        session.add(car)
        session.commit()
        return car, 201, self.make_response_headers(location=url_for('car', id=car.id, _external=True))
