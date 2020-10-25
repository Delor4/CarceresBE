from flask import url_for

from classes.auth import access_required, Rights
from classes.views import list_view
from db import session

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

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


class ZoneResource(Resource):
    """
    Resources for 'zone' (/api/zones/<id>) endpoint.
    """
    @access_required(Rights.USER)
    @marshal_with(zone_fields)
    def get(self, id):
        """
        Returns zone's data.
        """
        zone = session.query(Zone).filter(Zone.id == id).first()
        if not zone:
            abort(404, message="Zone {} doesn't exist".format(id))
        return zone

    @access_required(Rights.ADMIN)
    def delete(self, id):
        """
        Delete zone from database.
        """
        zone = session.query(Zone).filter(Zone.id == id).first()
        if not zone:
            abort(404, message="Zone {} doesn't exist".format(id))
        session.delete(zone)
        session.commit()
        return {}, 204

    @access_required(Rights.ADMIN)
    @marshal_with(zone_fields)
    def put(self, id):
        """
        Update zone's data.
        """
        parsed_args = parser.parse_args()
        zone = session.query(Zone).filter(Zone.id == id).first()
        zone.name = parsed_args['name']
        zone.bkg_file = parsed_args['bkg_file']
        session.add(zone)
        session.commit()
        return zone, 201


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
        return zone, 201
