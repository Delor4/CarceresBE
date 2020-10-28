from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import relationship

from classes.ModelBase import ModelBase


class Place(ModelBase):
    __tablename__ = 'places'

    nr = Column(Integer)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    name = Column(String(193), nullable=True)
    pos_x = Column(Float, nullable=True)
    pos_y = Column(Float, nullable=True)

    subscriptions = relationship("Subscription", backref="place.id")

    UniqueConstraint('nr', 'zone_id', name='uniq_place_1')
