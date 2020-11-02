from flask_restful import Resource
from flask_restful import abort
from sqlalchemy.exc import IntegrityError

from db import session


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

    def try_session_commit(self):
        try:
            session.flush()
        except IntegrityError as ex:
            session.rollback()
            abort(409, message=f"Integrity Error: {ex.orig}")
        session.commit()
