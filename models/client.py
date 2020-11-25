from sqlalchemy import Column, ForeignKey, Date
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from classes.ModelBase import ModelBase


class Client(ModelBase):
    __tablename__ = 'clients'

    name = Column(String(193))
    surname = Column(String(193))
    address = Column(String(193))
    city = Column(String(30))
    phone = Column(String(15))
    birthday = Column(Date(), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=True, default=None)
    user = relationship("User", back_populates="client", lazy='joined')

    cars = relationship("Car", backref="clients.id", cascade="all, delete", lazy='joined')
