from db import session

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

from models.zone import Zone

zone_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)


class ZoneResource(Resource):
    @marshal_with(zone_fields)
    def get(self, id):
        zone = session.query(Zone).filter(Zone.id == id).first()
        if not zone:
            abort(404, message="Zone {} doesn't exist".format(id))
        return zone

    def delete(self, id):
        zone = session.query(Zone).filter(Zone.id == id).first()
        if not zone:
            abort(404, message="Zone {} doesn't exist".format(id))
        session.delete(zone)
        session.commit()
        return {}, 204

    @marshal_with(zone_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        zone = session.query(Zone).filter(Zone.id == id).first()
        zone.name = parsed_args['name']
        session.add(zone)
        session.commit()
        return zone, 201


class ZoneListResource(Resource):
    @marshal_with(zone_fields)
    def get(self):
        zones = session.query(Zone).all()
        return zones

    @marshal_with(zone_fields)
    def post(self):
        parsed_args = parser.parse_args()
        zone = Zone(name=parsed_args['name'])
        session.add(zone)
        session.commit()
        return zone, 201
