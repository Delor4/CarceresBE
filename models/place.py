from datetime import datetime

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from base import Base


class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    nr = Column(Integer)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    name = Column(String(193), nullable=True)
    pos_x = Column(Float, nullable=True)
    pos_y = Column(Float, nullable=True)

    subscriptions = relationship("Subscription", backref="place.id")

    Column('created_on', DateTime(), default=datetime.now)
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)

    UniqueConstraint('nr', 'zone_id', name='uniq_place_1')
