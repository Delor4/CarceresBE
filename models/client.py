# !/usr/bin/env python
from sqlalchemy.orm import relationship

from base import Base
from sqlalchemy import Column
from sqlalchemy import Integer, String


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(193), unique=True)
    surname = Column(String(193))
    address = Column(String(193))
    city = Column(String(30))
    phone = Column(String(15))

    cars = relationship("Car", backref="clients.id")

    # TODO: add relation to user (nullable)
