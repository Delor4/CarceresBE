from flask import url_for
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse, inputs

from classes.SingleResource import SingleResource
from classes.auth import access_required, Rights
from classes.views import list_view, make_response_headers
from db import session
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


class SubscriptionResource(SingleResource):
    """
    Resources for 'subscription' (/api/subscriptions/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Subscription
        self.model_name = "Subscription"
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
        subscription.start = parsed_args['start']
        subscription.end = parsed_args['end']
        subscription.type = parsed_args['type']
        subscription.place_id = parsed_args['place_id']
        subscription.car_id = parsed_args['car_id']
        session.add(subscription)
        session.commit()
        return subscription, 201, self.make_response_headers(subscription)


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
        return subscription, 201, make_response_headers(subscription,
                                                        location=url_for('subscription', id=subscription.id,
                                                                         _external=True))
