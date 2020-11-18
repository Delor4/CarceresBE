from flask_restful import fields, inputs
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.ListResource import ListResource
from classes.SingleResource import SingleResource
from classes.auth import access_required, Rights
from models.payment import Payment

payment_fields = {
    'id': fields.Integer,
    'price': fields.Integer,
    'tax': fields.Integer,
    'value': fields.Integer,
    'sale_date': fields.DateTime,
    'paid_type': fields.Integer,
    'paid_date': fields.DateTime,
    'paid': fields.Boolean,
    'subscription_id': fields.Integer,
    'uri': fields.Url('payment', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('subscription_id', type=int, required=True, nullable=False)
parser.add_argument('price', type=int, required=True, nullable=False)
parser.add_argument('tax', type=int, required=True, nullable=False)
parser.add_argument('sale_date', type=inputs.datetime_from_iso8601, required=True, nullable=False)

parser_paid = reqparse.RequestParser()
parser_paid.add_argument('paid_type', type=int, required=True, nullable=False)
parser_paid.add_argument('paid_date', type=inputs.datetime_from_iso8601, required=False, nullable=True)


class PaymentResource(SingleResource):
    """
    Resources for 'invoice' (/api/payments/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Payment
        self.model_name = "payment"
        self.marshal_fields = payment_fields

    @access_required(Rights.USER)
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

    @access_required(Rights.ADMIN)
    @marshal_with(payment_fields)
    def put(self, id):
        """
        Update payment's data.
        """
        parsed_args = parser.parse_args()
        invoice = self.get_model(id)
        invoice.price = parsed_args['price']
        invoice.tax = parsed_args['tax']
        invoice.sale_date = parsed_args['sale_date']
        return self.finalize_put_req(invoice)


class PaymentListResource(ListResource):
    """
    Resources for 'payments' (/api/payments) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Payment
        self.model_name = "payment"
        self.marshal_fields = payment_fields

    @access_required(Rights.USER)
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
        payment = Payment(price=parsed_args['price'], tax=parsed_args['tax'], sale_date=parsed_args['sale_date'])
        return self.finalize_post_req(payment)
