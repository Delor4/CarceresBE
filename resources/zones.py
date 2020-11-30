from flask_restful import fields, abort, Resource
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.ListResource import ListResource
from classes.SingleResource import SingleResource
from classes.auth import access_required, Rights, nocache
from db import session
from models.place import Place
from models.zone import Zone

zone_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'bkg_file': fields.String,
    'places': fields.Nested({
        'id': fields.Integer,
        'nr': fields.Integer,
        'zone_id': fields.Integer,
        'name': fields.String,
        'pos_x': fields.Float,
        'pos_y': fields.Float,
        'occupied': fields.Boolean,
        'uri': fields.Url('place', absolute=True),
    }),
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
        self.model_name = "zone"
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
        return self.finalize_put_req(zone)


class ZoneListResource(ListResource):
    """
    Resources for 'zones' (/api/zones) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = Zone
        self.model_name = "zone"
        self.marshal_fields = zone_fields

    def get(self):
        """
        Returns data of all zones.
        """
        return self.process_get_req()

    @access_required(Rights.ADMIN)
    @marshal_with(zone_fields)
    def post(self):
        """
        Create new zone.
        """
        parsed_args = parser.parse_args()
        zone = Zone(name=parsed_args['name'], bkg_file=parsed_args['bkg_file'])
        return self.finalize_post_req(zone)


zone_info_fields = {
    'all': fields.Integer,
    'free': fields.Integer,
    'occupied': fields.Integer,
    'zone_id': fields.Integer,
}


class ZoneInfoResource(Resource):
    """
    Resources for 'zone' info (/api/zones/<id>/info) endpoint.
    """

    @nocache
    @marshal_with(zone_info_fields)
    def get(self, id):
        """
        Returns zone's info data.
        """
        model = session.query(Zone).filter(Zone.id == id).first()
        if not model:
            abort(404, message=f"{self.model_name.capitalize()} {id} doesn't exist")
        info = {}
        places_query = session.query(Place).filter(Place.zone_id == id)
        info['all'] = places_query.count()
        places = places_query.all()
        info['occupied'] = 0
        for place in places:
            if place.occupied:
                info['occupied'] += 1
        info['free'] = info['all'] - info['occupied']
        info['zone_id'] = id
        return info
