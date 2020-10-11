#!/usr/bin/env python
import os

from flask import send_file
from flask_cors import CORS
from flask_restful import Api

from classes.config import flask_app

app = flask_app
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

from resources.user import UserListResource, UserResource
from resources.place import PlaceListResource, PlaceResource
from resources.zone import ZoneListResource, ZoneResource
from resources.client import ClientListResource, ClientResource
from resources.car import CarListResource, CarResource
from resources.subscription import SubscriptionListResource, SubscriptionResource

api.add_resource(UserListResource, '/api/users', endpoint='users')
api.add_resource(UserResource, '/api/users/<string:id>', endpoint='user')

api.add_resource(ClientListResource, '/api/clients', endpoint='clients')
api.add_resource(ClientResource, '/api/clients/<string:id>', endpoint='client')

api.add_resource(CarListResource, '/api/cars', endpoint='cars')
api.add_resource(CarResource, '/api/cars/<string:id>', endpoint='car')

api.add_resource(ZoneListResource, '/api/zones', endpoint='zones')
api.add_resource(ZoneResource, '/api/zones/<string:id>', endpoint='zone')

api.add_resource(PlaceListResource, '/api/places', endpoint='places')
api.add_resource(PlaceResource, '/api/places/<string:id>', endpoint='place')

api.add_resource(SubscriptionListResource, '/api/subscriptions', endpoint='subscriptions')
api.add_resource(SubscriptionResource, '/api/subscriptions/<string:id>', endpoint='subscription')


# Everything not declared before (not a Flask route / API endpoint)...
@app.route("/<path:path>")
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, "index.html")
        return send_file(index_path)


if __name__ == '__main__':
    app.run(port=43343, debug=True)
