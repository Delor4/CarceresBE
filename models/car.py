from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from classes.ModelBase import ModelBase


class Car(ModelBase):
    __tablename__ = 'cars'

    plate = Column(String(12), unique=True)
    client_id = Column(Integer, ForeignKey("clients.id"))

    subscriptions = relationship("Subscription", backref="cars.id", lazy='joined')
