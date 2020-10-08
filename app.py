#!/usr/bin/env python
import os

from flask import Flask, send_file
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

from resources.user import UserListResource, UserResource
from resources.place import PlaceListResource, PlaceResource
from resources.zone import ZoneListResource, ZoneResource

api.add_resource(UserListResource, '/api/users', endpoint='users')
api.add_resource(UserResource, '/api/users/<string:id>', endpoint='user')

api.add_resource(ZoneListResource, '/api/zones', endpoint='zones')
api.add_resource(ZoneResource, '/api/zones/<string:id>', endpoint='zone')

api.add_resource(PlaceListResource, '/api/places', endpoint='places')
api.add_resource(PlaceResource, '/api/places/<string:id>', endpoint='place')


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
