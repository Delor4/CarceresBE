from flask import url_for

from classes.auth import access_required, Rights
from classes.views import list_view, make_time_headers
from db import session

from flask_restful import reqparse, inputs
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

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
parser.add_argument('start', type=inputs.datetime_from_iso8601, required=True, nullable=False)
parser.add_argument('end', type=inputs.datetime_from_iso8601, required=True, nullable=False)
parser.add_argument('type', type=int, required=True, nullable=False)
parser.add_argument('place_id', type=int, required=True, nullable=False)
parser.add_argument('car_id', type=int, required=True, nullable=False)


class SubscriptionResource(Resource):
    """
    Resources for 'subscription' (/api/subscriptions/<id>) endpoint.
    """

    @access_required(Rights.MOD)
    @marshal_with(subscription_fields)
    def get(self, id):
        """
        Returns subscription's data.
        """
        subscription = session.query(Subscription).filter(Subscription.id == id).first()
        if not subscription:
            abort(404, message="Subscription {} doesn't exist".format(id))
        return subscription, 200, make_time_headers(subscription)

    @access_required(Rights.MOD)
    def delete(self, id):
        """
        Delete subscription from database.
        """
        subscription = session.query(Subscription).filter(Subscription.id == id).first()
        if not subscription:
            abort(404, message="Subscription {} doesn't exist".format(id))
        session.delete(subscription)
        session.commit()
        return {}, 204

    @access_required(Rights.MOD)
    @marshal_with(subscription_fields)
    def put(self, id):
        """
        Update subscription's data.
        """
        parsed_args = parser.parse_args()
        subscription = session.query(Subscription).filter(Subscription.id == id).first()
        subscription.start = parsed_args['start']
        subscription.end = parsed_args['end']
        subscription.type = parsed_args['type']
        subscription.place_id = parsed_args['place_id']
        subscription.car_id = parsed_args['car_id']
        session.add(subscription)
        session.commit()
        return subscription, 201, make_time_headers(subscription)


class SubscriptionListResource(Resource):
    """
    Resources for 'subscriptions' (/api/subscriptions) endpoint.
    """

    @access_required(Rights.MOD)
    def get(self):
        """
        Returns data of all subscriptions.
        """
        return list_view(Subscription, subscription_fields, url_for(self.endpoint, _external=True))

    @access_required(Rights.MOD)
    @marshal_with(subscription_fields)
    def post(self):
        """
        Create new subscription.
        """
        parsed_args = parser.parse_args()
        subscription = Subscription(start=parsed_args['start'],
                                    end=parsed_args['end'],
                                    type=parsed_args['type'],
                                    place_id=parsed_args['place_id'],
                                    car_id=parsed_args['car_id']
                                    )
        session.add(subscription)
        session.commit()
        return subscription, 201
