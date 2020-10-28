from flask import url_for
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.SingleResource import SingleResource
from classes.auth import access_required, Rights
from classes.views import list_view, make_response_headers
from db import session
from models.zone import Zone
from resources.places import place_fields

zone_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'bkg_file': fields.String,
    'places': fields.Nested(place_fields),
    'uri': fields.Url('zone', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('bkg_file', type=str)


class ZoneResource(SingleResource):
    """
    Resources for 'zone' (/api/zones/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Zone
        self.model_name = "Zone"
        self.marshal_fields = zone_fields

    @access_required(Rights.USER)
    @marshal_with(zone_fields)
    def get(self, id):
        """
        Returns zone's data.
        """
        return self.process_get_req(id)

    @access_required(Rights.ADMIN)
    def delete(self, id):
        """
        Delete zone from database.
        """
        return self.process_delete_req(id)

    @access_required(Rights.ADMIN)
    @marshal_with(zone_fields)
    def put(self, id):
        """
        Update zone's data.
        """
        parsed_args = parser.parse_args()
        zone = self.get_model(id)
        zone.name = parsed_args['name']
        zone.bkg_file = parsed_args['bkg_file']
        session.add(zone)
        session.commit()
        return zone, 201, self.make_response_headers(zone)


class ZoneListResource(Resource):
    """
    Resources for 'zones' (/api/zones) endpoint.
    """

    @access_required(Rights.USER)
    def get(self):
        """
        Returns data of all zones.
        """
        return list_view(Zone, zone_fields, url_for(self.endpoint, _external=True))

    @access_required(Rights.ADMIN)
    @marshal_with(zone_fields)
    def post(self):
        """
        Create new zone.
        """
        parsed_args = parser.parse_args()
        zone = Zone(name=parsed_args['name'], bkg_file=parsed_args['bkg_file'])
        session.add(zone)
        session.commit()
        return zone, 201, make_response_headers(zone, location=url_for('zone', id=zone.id, _external=True))
