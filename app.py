#!/usr/bin/env python
import os

from flask import send_file, Flask
from flask_cors import CORS
from flask_restful import Api

from classes.auth import get_auth_token, refresh_token
from classes.config import config

app = Flask(__name__)
app.config.from_mapping(config)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)


@app.route('/api/login')
def login():
    return get_auth_token()


@app.route('/api/refresh', methods=['POST'])
def refresh():
    return refresh_token()


from resources.manage import UserManageResource, ClientManageResource

api.add_resource(UserManageResource, '/api/user', endpoint='user_manage')
api.add_resource(ClientManageResource, '/api/client', endpoint='client_manage')

from resources.users import UserListResource, UserResource

api.add_resource(UserListResource, '/api/users', endpoint='users')
api.add_resource(UserResource, '/api/users/<string:id>', endpoint='user')

from resources.clients import ClientListResource, ClientResource

api.add_resource(ClientListResource, '/api/clients', endpoint='clients')
api.add_resource(ClientResource, '/api/clients/<string:id>', endpoint='client')

from resources.cars import CarListResource, CarResource

api.add_resource(CarListResource, '/api/cars', endpoint='cars')
api.add_resource(CarResource, '/api/cars/<string:id>', endpoint='car')

from resources.zones import ZoneListResource, ZoneResource

api.add_resource(ZoneListResource, '/api/zones', endpoint='zones')
api.add_resource(ZoneResource, '/api/zones/<string:id>', endpoint='zone')

from resources.places import PlaceListResource, PlaceResource

api.add_resource(PlaceListResource, '/api/places', endpoint='places')
api.add_resource(PlaceResource, '/api/places/<string:id>', endpoint='place')

from resources.subscriptions import SubscriptionListResource, SubscriptionResource

api.add_resource(SubscriptionListResource, '/api/subscriptions', endpoint='subscriptions')
api.add_resource(SubscriptionResource, '/api/subscriptions/<string:id>', endpoint='subscription')

if app.debug:
    from resources.seed import SeedResource

    api.add_resource(SeedResource, '/api/seed', endpoint='seed')


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
