from flask_restful import abort

from classes.ResourceBase import ResourceBase
from db import session


class SingleResource(ResourceBase):
    __abstract__ = True

    def __init__(self):
        super(SingleResource, self).__init__()
        self.model_class = None
        self.model_name = None
        self.marshal_fields = None

    def get_model(self, model_id):
        """
        Get and return model from the database. Return 404 when model is absent.
        """
        model = session.query(self.model_class).filter(self.model_class.id == model_id).first()
        if not model:
            abort(404, message=f"{self.model_name} {model_id} doesn't exist")
        return model

    def process_get_req(self, model_id):
        """
        Return model from the database. 404 when model is absent.
        """
        model = self.get_model(model_id)
        return model, 200, self.make_response_headers(model)

    def process_delete_req(self, model_id):
        """
        Delete model from the database. Return 404 when model is absent.
        """
        model = self.get_model(model_id)
        session.delete(model)
        session.commit()
        return {}, 204

    def finalize_put_req(self, model):
        """
        Save model in database. Return to client with appropriate status code and headers.
        """
        session.add(model)
        session.commit()
        return model, 201, self.make_response_headers(model)
