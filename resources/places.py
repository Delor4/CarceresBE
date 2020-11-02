from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.ListResource import ListResource
from classes.SingleResource import SingleResource
from classes.auth import access_required, Rights
from db import session
from models.place import Place
from models.zone import Zone

place_fields = {
    'id': fields.Integer,
    'nr': fields.Integer,
    'zone_id': fields.Integer,
    'name': fields.String,
    'pos_x': fields.Float,
    'pos_y': fields.Float,
    'uri': fields.Url('place', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('nr', type=int, required=True, nullable=False)
parser.add_argument('zone_id', type=int, required=True, nullable=False)
parser.add_argument('name', type=str, required=False, nullable=True)
parser.add_argument('pos_x', type=float, required=False, nullable=True)
parser.add_argument('pos_y', type=float, required=False, nullable=True)


class PlaceResource(SingleResource):
    """
    Resources for 'place' (/api/places/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Place
        self.model_name = "place"
        self.marshal_fields = place_fields

    @access_required(Rights.USER)
    @marshal_with(place_fields)
    def get(self, id):
        """
        Returns place's data.
        """
        return self.process_get_req(id)

    @access_required(Rights.ADMIN)
    def delete(self, id):
        """
        Delete place from database.
        """
        return self.process_delete_req(id)

    @access_required(Rights.ADMIN)
    @marshal_with(place_fields)
    def put(self, id):
        """
        Update place's data.
        """
        parsed_args = parser.parse_args()
        place = self.get_model(id)
        place.nr = parsed_args['nr']
        place.name = parsed_args['name']
        place.pos_x = parsed_args['pos_x']
        place.pos_y = parsed_args['pos_y']
        place.zone_id = parsed_args['zone_id']
        zone = session.query(Zone).filter(Zone.id == parsed_args['zone_id']).first()
        if not zone:
            abort(404, message=f"Zone {parsed_args['zone_id']} doesn't exist")
        zone.places.append(place)
        return self.finalize_put_req(place)


class PlaceListResource(ListResource):
    """
    Resources for 'places' (/api/places/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Place
        self.model_name = "place"
        self.marshal_fields = place_fields

    @access_required(Rights.USER)
    def get(self):
        """
        Returns data of all places.
        """
        return self.process_get_req()

    @access_required(Rights.ADMIN)
    @marshal_with(place_fields)
    def post(self):
        """
        Create new place.
        """
        parsed_args = parser.parse_args()
        place = Place(nr=parsed_args['nr'], zone_id=parsed_args['zone_id'], name=parsed_args['name'],
                      pos_x=parsed_args['pos_x'], pos_y=parsed_args['pos_y'])
        zone = session.query(Zone).filter(Zone.id == parsed_args['zone_id']).first()
        zone.places.append(place)
        return self.finalize_post_req(place)
