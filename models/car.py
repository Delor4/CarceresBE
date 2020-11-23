from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from classes.ModelBase import ModelBase


class Car(ModelBase):
    __tablename__ = 'cars'

    plate = Column(String(12), unique=True)
    brand = Column(String(50), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", uselist=False,  lazy='joined')
