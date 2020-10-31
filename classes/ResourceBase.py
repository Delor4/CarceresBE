from flask_restful import Resource


class ResourceBase(Resource):
    __abstract__ = True

    @staticmethod
    def make_response_headers(location=None):
        """
        Return additional response headers.
        """
        headers = {

        }
        if location is not None:
            headers['Location'] = location
        return headers
