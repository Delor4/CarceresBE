from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.ListResource import ListResource
from classes.SingleResource import SingleResource
from classes.auth import access_required, Rights
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
