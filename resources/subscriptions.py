from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse, inputs

from classes.ListResource import ListResource
from classes.SingleResource import SingleResource
from classes.auth import access_required, Rights
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
parser.add_argument('start', type=inputs.datetime_from_iso8601, required=False, nullable=False)
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
        parsed_args = parser.parse_args()
        subscription = Subscription(
            end=parsed_args['end'],
            type=parsed_args['type'],
            place_id=parsed_args['place_id'],
            car_id=parsed_args['car_id']
        )
        if parsed_args['start']:
            subscription.start = parsed_args['start']
        return self.finalize_post_req(subscription)
