from datetime import timezone
from email.utils import format_datetime

from flask_restful import Resource


class ResourceBase(Resource):
    __abstract__ = True

    @staticmethod
    def make_response_headers(obj, location=None):
        """
        Return additional response headers.
        """
        d = obj.updated_on
        headers = {
            "Last-Modified": format_datetime(d.replace(tzinfo=timezone.utc), usegmt=True)
        }
        if location is not None:
            headers['Location'] = location
        return headers
