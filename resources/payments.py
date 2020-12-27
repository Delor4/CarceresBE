from datetime import datetime

import pytz
from flask_restful import fields, inputs, abort
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.ListResource import ListResource
from classes.SingleResource import SingleResource
from classes.auth import (
    access_required,
    Rights,
    auth,
    token_required,
    set_last_modified,
)
from db import session
from models.car import Car
from models.client import Client
from models.payment import Payment, PaidTypes
from models.subscription import Subscription

payment_fields = {
    "id": fields.Integer,
    "price": fields.Integer,
    "tax": fields.Integer,
    "value": fields.Integer,
    "sale_date": fields.DateTime,
    "paid_type": fields.Integer,
    "paid_date": fields.DateTime,
    "paid": fields.Boolean,
    "subscription_id": fields.Integer,
    "uri": fields.Url("payment", absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument("subscription_id", type=int, required=True, nullable=False)
parser.add_argument("price", type=int, required=True, nullable=False)
parser.add_argument("tax", type=int, required=True, nullable=False)
parser.add_argument(
    "sale_date", type=inputs.datetime_from_iso8601, required=True, nullable=False
)

parser_paid = reqparse.RequestParser()
parser_paid.add_argument("paid_type", type=int, required=True, nullable=False)
parser_paid.add_argument(
    "paid_date", type=inputs.datetime_from_iso8601, required=False, nullable=True
)


class PaymentResource(SingleResource):
    """
    Resources for 'invoice' (/api/payments/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Payment
        self.model_name = "payment"
        self.marshal_fields = payment_fields

    @access_required(Rights.MOD)
    @marshal_with(payment_fields)
    def get(self, id):
        """
        Returns payment's data.
        """
        return self.process_get_req(id)

    @access_required(Rights.ADMIN)
    def delete(self, id):
        """
        Delete payment from database.
        """
        return self.process_delete_req(id)

    @access_required(Rights.MOD)
    @marshal_with(payment_fields)
    def put(self, id):
        """
        Update payment's data (only paid status).
        """
        parsed_args = parser_paid.parse_args()
        payment = self.get_model(id)
        payment.paid_type = parsed_args["paid_type"]
        if (
            parsed_args["paid_date"] is None
            and parsed_args["paid_type"] != PaidTypes.NONE
        ):
            payment.paid_date = datetime.utcnow().replace(tzinfo=pytz.UTC)
        else:
            payment.paid_date = parsed_args["paid_date"]
        return self.finalize_put_req(payment)


class PaymentListResource(ListResource):
    """
    Resources for 'payments' (/api/payments) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Payment
        self.model_name = "payment"
        self.marshal_fields = payment_fields

    @access_required(Rights.MOD)
    def get(self):
        """
        Returns data of all payments.
        """
        return self.process_get_req()

    @access_required(Rights.ADMIN)
    @marshal_with(payment_fields)
    def post(self):
        """
        Create new payment.
        """
        parsed_args = parser.parse_args()
        payment = Payment(
            price=parsed_args["price"],
            tax=parsed_args["tax"],
            sale_date=parsed_args["sale_date"],
        )
        return self.finalize_post_req(payment)


class PaymentListOwnResource(ListResource):
    """
    Resources for 'own_payments' (/api/client/payments) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Payment
        self.model_name = "payment"
        self.marshal_fields = payment_fields

    @token_required
    def get(self):
        """
        Returns the payments of the currently authenticated client.
        """
        client = session.query(Client).filter(Client.user_id == auth.user.id).first()
        if not client:
            abort(404, message="Client doesn't exist")
        return self.process_get_req(
            session.query(Payment)
            .join(Subscription)
            .filter(Payment.subscription_id == Subscription.id)
            .join(Car)
            .filter(Subscription.car_id == Car.id)
            .filter(Car.client_id == client.id)
        )


class PaymentOwnResource(SingleResource):
    """
    Resources for 'own_payment' (/api/client/payments/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Payment
        self.model_name = "payment"
        self.marshal_fields = payment_fields

    @token_required
    @marshal_with(payment_fields)
    @set_last_modified
    def get(self, id):
        """
        Returns the payment of the currently authenticated client.
        """
        client = session.query(Client).filter(Client.user_id == auth.user.id).first()
        if not client:
            abort(404, message="Client doesn't exist")
        payment = (
            session.query(Payment)
            .filter(Payment.id == id)
            .join(Subscription)
            .filter(Payment.subscription_id == Subscription.id)
            .join(Car)
            .filter(Subscription.car_id == Car.id)
            .filter(Car.client_id == client.id)
            .first()
        )
        if not payment:
            abort(404, message=f"{self.model_name.capitalize()} {id} doesn't exist")
        return payment, 200

    @token_required
    @marshal_with(payment_fields)
    def put(self, id):
        """
        Update own payment.
        """
        # TODO: delete this method and implement online payments
        # Checks
        client = session.query(Client).filter(Client.user_id == auth.user.id).first()
        if not client:
            abort(404, message="Client doesn't exist")

        payment = (
            session.query(Payment)
            .filter(self.model_class.id == id)
            .join(Subscription)
            .filter(Payment.subscription_id == Subscription.id)
            .join(Car)
            .filter(Subscription.car_id == Car.id)
            .filter(Car.client_id == client.id)
            .first()
        )
        if not payment:
            abort(404, message=f"{self.model_name.capitalize()} {id} doesn't exist")

        payment.paid_type = PaidTypes.ONLINE
        payment.paid_date = datetime.utcnow().replace(tzinfo=pytz.UTC)

        return self.finalize_put_req(payment)
