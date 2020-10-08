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
    'name': fields.String,
    'pos_x': fields.Float,
    'pos_y': fields.Float,
}

parser = reqparse.RequestParser()
parser.add_argument('nr', type=int, required=True, nullable=False)
parser.add_argument('zone_id', type=int, required=True, nullable=False)
parser.add_argument('name', type=str, required=False, nullable=True)
parser.add_argument('pos_x', type=float, required=False, nullable=True)
parser.add_argument('pos_y', type=float, required=False, nullable=True)


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
        place.zone_id = parsed_args['zone_id']
        place.name = parsed_args['name']
        place.pos_x = parsed_args['pos_x']
        place.pos_y = parsed_args['pos_y']
        zone = session.query(Zone).filter(Zone.id == parsed_args['zone_id']).first()
        zone.places.append(place)
        session.add(place)
        session.commit()
        return place, 201


class PlaceListResource(Resource):
    @marshal_with(place_fields)
    def get(self):
        places = session.query(Place).all()
        return places

    @marshal_with(place_fields)
    def post(self):
        parsed_args = parser.parse_args()
        place = Place(nr=parsed_args['nr'], zone_id=parsed_args['zone_id'], name=parsed_args['name'],
                      pos_x=parsed_args['pos_x'], pos_y=parsed_args['pos_y'])
        zone = session.query(Zone).filter(Zone.id == parsed_args['zone_id']).first()
        zone.places.append(place)
        session.add(place)
        session.commit()
        return place, 201
