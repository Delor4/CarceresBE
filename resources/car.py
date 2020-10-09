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
    @marshal_with(car_fields)
    def get(self, id):
        car = session.query(Car).filter(Car.id == id).first()
        if not car:
            abort(404, message="Car {} doesn't exist".format(id))
        return car

    def delete(self, id):
        car = session.query(Car).filter(Car.id == id).first()
        if not car:
            abort(404, message="Car {} doesn't exist".format(id))
        session.delete(car)
        session.commit()
        return {}, 204

    @marshal_with(car_fields)
    def put(self, id):
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
    @marshal_with(car_fields)
    def get(self):
        cars = session.query(Car).all()
        return cars

    @marshal_with(car_fields)
    def post(self):
        parsed_args = parser.parse_args()
        car = Car(plate=parsed_args['plate'], client_id=parsed_args['client_id'])
        client = session.query(Client).filter(Client.id == parsed_args['client_id']).first()
        client.cars.append(car)
        session.add(car)
        session.commit()
        return car, 201
