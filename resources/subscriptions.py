from datetime import datetime

import pytz
from flask_restful import fields, abort
from flask_restful import marshal_with
from flask_restful import reqparse, inputs

from classes.ListResource import ListResource
from classes.SingleResource import SingleResource
from classes.auth import access_required, Rights, token_required, auth
from db import session
from models.car import Car
from models.client import Client
from models.place import Place
from models.subscription import Subscription

subscription_fields = {
    'id': fields.Integer,
    'start': fields.DateTime,
    'end': fields.DateTime,
    'type': fields.Integer,
    'place_id': fields.Integer,
    'car_id': fields.Integer,
    'uri': fields.Url('subscription', absolute=True),
}

parser = reqparse.RequestParser()
# parser.add_argument('start', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
parser.add_argument('start', type=inputs.datetime_from_iso8601, required=False, nullable=True)
parser.add_argument('end', type=inputs.datetime_from_iso8601, required=True, nullable=False)
parser.add_argument('type', type=int, required=True, nullable=False)
parser.add_argument('place_id', type=int, required=True, nullable=False)
parser.add_argument('car_id', type=int, required=True, nullable=False)


class SubscriptionResource(SingleResource):
    """
    Resources for 'subscription' (/api/subscriptions/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Subscription
        self.model_name = "subscription"
        self.marshal_fields = subscription_fields

    @access_required(Rights.MOD)
    @marshal_with(subscription_fields)
    def get(self, id):
        """
        Returns subscription's data.
        """
        return self.process_get_req(id)

    @access_required(Rights.MOD)
    def delete(self, id):
        """
        Delete subscription from database.
        """
        return self.process_delete_req(id)

    @access_required(Rights.MOD)
    @marshal_with(subscription_fields)
    def put(self, id):
        """
        Update subscription's data.
        """
        parsed_args = parser.parse_args()
        subscription = self.get_model(id)
        if parsed_args['start']:
            subscription.start = parsed_args['start']
        subscription.end = parsed_args['end']
        subscription.type = parsed_args['type']
        subscription.place_id = parsed_args['place_id']
        subscription.car_id = parsed_args['car_id']
        return self.finalize_put_req(subscription)


class SubscriptionListResource(ListResource):
    """
    Resources for 'subscriptions' (/api/subscriptions) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Subscription
        self.model_name = "subscription"
        self.marshal_fields = subscription_fields

    @access_required(Rights.MOD)
    def get(self):
        """
        Returns data of all subscriptions.
        """
        return self.process_get_req()

    @access_required(Rights.MOD)
    @marshal_with(subscription_fields)
    def post(self):
        """
        Create new subscription.
        """
        # Checks
        parsed_args = parser.parse_args()
        car = session.query(Car).filter(Car.id == parsed_args['car_id']).first()
        if not car:
            abort(400, message="No car.")
        place = session.query(Place).filter(Place.id == parsed_args['place_id']).first()
        if not place or place.occupied:
            abort(400, message="Place not allowed.")
        if parsed_args['end'] <= datetime.utcnow().replace(tzinfo=pytz.UTC):
            abort(400, message="End date in past.")

        subscription = Subscription(
            end=parsed_args['end'],
            type=parsed_args['type'],
            place_id=parsed_args['place_id'],
            car_id=parsed_args['car_id']
        )
        if parsed_args['start']:
            subscription.start = parsed_args['start']
        return self.finalize_post_req(subscription)


class SubscriptionOwnResource(ListResource):
    """
    Resources for 'own_subscriptions' (/api/client/subscriptions) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Subscription
        self.model_name = "subscription"
        self.marshal_fields = subscription_fields

    @token_required
    def get(self):
        """
        Returns the subscriptions data of the currently authenticated client.
        """
        client = session.query(Client).filter(Client.user_id == auth.user.id).first()
        if not client:
            abort(404, message="Client doesn't exist")
        return self.process_get_req(session.query(Subscription)
                                    .join(Car).filter(Subscription.car_id == Car.id)
                                    .filter(Car.client_id == client.id))

    @token_required
    @marshal_with(subscription_fields)
    def post(self):
        """
        Create new subscription.
        """
        # Checks
        parsed_args = parser.parse_args()
        client = session.query(Client).filter(Client.user_id == auth.user.id).first()
        if not client:
            abort(404, message="Client doesn't exist")
        car = session.query(Car).filter(Car.id == parsed_args['car_id']).first()
        if not car or car.client_id != client.id:
            abort(400, message="Not client's car.")
        place = session.query(Place).filter(Place.id == parsed_args['place_id']).first()
        if not place or place.occupied:
            abort(400, message="Place not allowed.")
        if parsed_args['end'] <= datetime.utcnow().replace(tzinfo=pytz.UTC):
            abort(400, message="End date in past.")

        subscription = Subscription(
            end=parsed_args['end'],
            type=parsed_args['type'],
            place_id=place.id,
            car_id=car.id
        )
        return self.finalize_post_req(subscription)
