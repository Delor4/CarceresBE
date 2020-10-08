#!/usr/bin/env python

from base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

class Zone(Base):
    __tablename__ = 'zones'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    places = relationship("Place", backref="zones.id")
