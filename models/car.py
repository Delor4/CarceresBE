from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String

from classes.ModelBase import ModelBase


class Car(ModelBase):
    __tablename__ = 'cars'

    plate = Column(String(12), unique=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
