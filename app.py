#!/usr/bin/env python
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import send_file, Flask
from flask_cors import CORS
from flask_restful import Api

from classes.auth import get_auth_tokens, refresh_token
from classes.config import config
from send_emails import setup_scheduler

app = Flask(__name__)
app.config.from_mapping(config)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

setup_scheduler(app)


@app.route("/api/login")
def login():
    """
    Authenticate (basic auth) and returns pair of access/refresh tokens.
    """
    return get_auth_tokens()


@app.route("/api/refresh", methods=["POST"])
def refresh():
    """
    Authenticate (refresh token) and returns new pair of access/refresh tokens.
    """
    return refresh_token()


from resources.manage import UserManageResource, ClientManageResource

api.add_resource(UserManageResource, "/api/user", endpoint="user_manage")
api.add_resource(ClientManageResource, "/api/client", endpoint="client_manage")

from resources.users import UserListResource, UserResource

api.add_resource(UserListResource, "/api/users", endpoint="users")
api.add_resource(UserResource, "/api/users/<string:id>", endpoint="user")

from resources.clients import ClientListResource, ClientResource

api.add_resource(ClientListResource, "/api/clients", endpoint="clients")
api.add_resource(ClientResource, "/api/clients/<string:id>", endpoint="client")

from resources.cars import (
    CarListResource,
    CarResource,
    CarListOwnResource,
    CarOwnResource,
)

api.add_resource(CarListResource, "/api/cars", endpoint="cars")
api.add_resource(CarResource, "/api/cars/<string:id>", endpoint="car")
api.add_resource(CarListOwnResource, "/api/client/cars", endpoint="own_cars")
api.add_resource(CarOwnResource, "/api/client/cars/<string:id>", endpoint="own_car")

from resources.zones import ZoneListResource, ZoneResource, ZoneInfoResource

api.add_resource(ZoneListResource, "/api/zones", endpoint="zones")
api.add_resource(ZoneResource, "/api/zones/<string:id>", endpoint="zone")
api.add_resource(ZoneInfoResource, "/api/zones/<string:id>/info", endpoint="zone_info")

from resources.places import PlaceListResource, PlaceResource

api.add_resource(PlaceListResource, "/api/places", endpoint="places")
api.add_resource(PlaceResource, "/api/places/<string:id>", endpoint="place")

from resources.payments import (
    PaymentListResource,
    PaymentResource,
    PaymentListOwnResource,
    PaymentOwnResource,
)

api.add_resource(PaymentListResource, "/api/payments", endpoint="payments")
api.add_resource(PaymentResource, "/api/payments/<string:id>", endpoint="payment")
api.add_resource(
    PaymentListOwnResource, "/api/client/payments", endpoint="own_payments"
)
api.add_resource(
    PaymentOwnResource, "/api/client/payments/<string:id>", endpoint="own_payment"
)

from resources.subscriptions import SubscriptionListResource, SubscriptionResource
from resources.subscriptions import SubscriptionListOwnResource, SubscriptionOwnResource

api.add_resource(
    SubscriptionListResource, "/api/subscriptions", endpoint="subscriptions"
)
api.add_resource(
    SubscriptionResource, "/api/subscriptions/<string:id>", endpoint="subscription"
)
api.add_resource(
    SubscriptionListOwnResource,
    "/api/client/subscriptions",
    endpoint="own_subscriptions",
)
api.add_resource(
    SubscriptionOwnResource,
    "/api/client/subscriptions/<string:id>",
    endpoint="own_subscription",
)

if app.debug:
    from resources.seed import SeedResource

    api.add_resource(SeedResource, "/api/seed", endpoint="seed")


# Everything not declared before (not a Flask route / API endpoint)...
@app.route("/<path:path>")
def route_frontend(path):
    """
    Returns frontend file if path is not backends.
    """
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, "index.html")
        return send_file(index_path)


if __name__ == "__main__":
    app.run(port=43343, debug=True)
