from classes.auth import access_required, Rights
from db import session

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

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


class CarResource(Resource):
    """
    Resources for 'car' (/api/cars/<id>) endpoint.
    """
    @access_required(Rights.MOD)
    @marshal_with(car_fields)
    def get(self, id):
        """
        Returns car's data.
        """
        car = session.query(Car).filter(Car.id == id).first()
        if not car:
            abort(404, message="Car {} doesn't exist".format(id))
        return car

    @access_required(Rights.MOD)
    def delete(self, id):
        """
        Delete car from database.
        """
        car = session.query(Car).filter(Car.id == id).first()
        if not car:
            abort(404, message="Car {} doesn't exist".format(id))
        session.delete(car)
        session.commit()
        return {}, 204

    @access_required(Rights.MOD)
    @marshal_with(car_fields)
    def put(self, id):
        """
        Update car's data.
        """
        parsed_args = parser.parse_args()
        car = session.query(Car).filter(Car.id == id).first()
        car.plate = parsed_args['plate']
        car.client_id = parsed_args['client_id']
        client = session.query(Client).filter(Client.id == parsed_args['client_id']).first()
        client.places.append(car)
        session.add(car)
        session.commit()
        return car, 201


class CarListResource(Resource):
    """
    Resources for 'cars' (/api/cars) endpoint.
    """
    @access_required(Rights.MOD)
    @marshal_with(car_fields)
    def get(self):
        """
        Returns data of all cars.
        """
        cars = session.query(Car).all()
        return cars

    @access_required(Rights.MOD)
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
        return car, 201
