#!/usr/bin/env python

from base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer


class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    nr = Column(Integer)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    # TODO: 'nr', 'zone_id' - unique pair
    # TODO: add field 'name' - nullable
