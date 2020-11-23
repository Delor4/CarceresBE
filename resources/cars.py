from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.ListResource import ListResource
from classes.SingleResource import SingleResource
from classes.auth import access_required, Rights, token_required, auth, set_last_modified
from db import session
from models.car import Car
from models.client import Client

car_fields = {
    'id': fields.Integer,
    'plate': fields.String,
    'brand': fields.String,
    'client_id': fields.Integer,
    'client': fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'surname': fields.String,
        'address': fields.String,
        'city': fields.String,
        'phone': fields.String,
        'user_id': fields.Integer,
        'uri': fields.Url('client', absolute=True),
    }),
    'uri': fields.Url('car', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('plate', type=str, required=True, nullable=False)
parser.add_argument('brand', type=str, required=False, nullable=True)
parser.add_argument('client_id', type=int, required=True, nullable=False)


class CarResource(SingleResource):
    """
    Resources for 'car' (/api/cars/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Car
        self.model_name = "car"
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
        car.brand = parsed_args['brand']
        car.client_id = parsed_args['client_id']
        client = session.query(Client).filter(Client.id == parsed_args['client_id']).first()
        if not client:
            abort(404, message=f"Client {parsed_args['client_id']} doesn't exist")
        client.cars.append(car)
        return self.finalize_put_req(car)


class CarListResource(ListResource):
    """
    Resources for 'cars' (/api/cars) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Car
        self.model_name = "car"
        self.marshal_fields = car_fields

    @access_required(Rights.MOD)
    def get(self):
        """
        Returns data of all cars.
        """
        return self.process_get_req()

    @access_required(Rights.MOD)
    @marshal_with(car_fields)
    def post(self):
        """
        Create new car.
        """
        parsed_args = parser.parse_args()
        car = Car(plate=parsed_args['plate'], client_id=parsed_args['client_id'], brand=parsed_args['brand'])

        client = session.query(Client).filter(Client.id == parsed_args['client_id']).first()
        client.cars.append(car)
        return self.finalize_post_req(car)


class CarListOwnResource(ListResource):
    """
    Resources for 'own_cars' (/api/client/cars) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Car
        self.model_name = "car"
        self.marshal_fields = car_fields

    @token_required
    def get(self):
        """
        Returns the cars data of the currently authenticated client.
        """
        client = session.query(Client).filter(Client.user_id == auth.user.id).first()
        if not client:
            abort(404, message="Client doesn't exist")
        return self.process_get_req(session.query(Car).filter(Car.client_id == client.id))


class CarOwnResource(SingleResource):
    """
      Resources for 'own_car' (/api/client/cars/<id>) endpoint.
      """

    def __init__(self):
        super().__init__()
        self.model_class = Car
        self.model_name = "car"
        self.marshal_fields = car_fields

    @token_required
    @marshal_with(car_fields)
    @set_last_modified
    def get(self, id):
        """
        Returns the car of the currently authenticated client.
        """
        client = session.query(Client).filter(Client.user_id == auth.user.id).first()
        if not client:
            abort(404, message="Client doesn't exist")
        car = session.query(Car).filter(id == Car.id).filter(Car.client_id == client.id).first()
        if not car:
            abort(404, message=f"{self.model_name.capitalize()} {id} doesn't exist")
        return car, 200
