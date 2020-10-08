from db import session

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

from models.zone import Zone
from models.place import Place

place_fields = {
    'id': fields.Integer,
    'nr': fields.Integer,
    'uri': fields.Url('place', absolute=True),
    'zone_id': fields.Integer,
}

parser = reqparse.RequestParser()
parser.add_argument('nr', type=int)
parser.add_argument('zone_id', type=int)


class PlaceResource(Resource):
    @marshal_with(place_fields)
    def get(self, id):
        place = session.query(Place).filter(Place.id == id).first()
        if not place:
            abort(404, message="Place {} doesn't exist".format(id))
        return place

    def delete(self, id):
        place = session.query(Place).filter(Place.id == id).first()
        if not place:
            abort(404, message="Place {} doesn't exist".format(id))
        session.delete(place)
        session.commit()
        return {}, 204

    @marshal_with(place_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        place = session.query(Place).filter(Place.id == id).first()
        place.nr = parsed_args['nr']
        zone = session.query(Zone).filter(Zone.id == parsed_args['zone_id']).first()
        zone.places.append(place)
        session.add(place)
        session.commit()
        return place, 201


class PlaceListResource(Resource):
    @marshal_with(place_fields)
    def get(self):
        place = session.query(Place).all()
        return place

    @marshal_with(place_fields)
    def post(self):
        parsed_args = parser.parse_args()
        place = Place(nr=parsed_args['nr'], zone_id=parsed_args['zone_id'])
        zone = session.query(Zone).filter(Zone.id == parsed_args['zone_id']).first()
        zone.places.append(place)
        session.add(place)
        session.commit()
        return place, 201
