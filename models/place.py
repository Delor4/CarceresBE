from datetime import datetime

from sqlalchemy import Column, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import relationship

from classes.ModelBase import ModelBase


class Place(ModelBase):
    __tablename__ = "places"

    nr = Column(Integer)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    zone = relationship("Zone", uselist=False, lazy="joined")

    name = Column(String(193), nullable=True)
    pos_x = Column(Float, nullable=True)
    pos_y = Column(Float, nullable=True)
    blocked = Column(Boolean, nullable=False, default=False)

    subscriptions = relationship("Subscription", backref="place.id", lazy="joined")

    UniqueConstraint("nr", "zone_id", name="uniq_place_1")

    @property
    def occupied(self):
        if self.blocked:
            return True
        now = datetime.utcnow()
        for subs in self.subscriptions:
            if subs.end >= now:
                return True
        return False
