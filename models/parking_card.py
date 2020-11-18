from sqlalchemy import Column, Boolean
from sqlalchemy.orm import relationship

from classes.ModelBase import ModelBase


class ParkingCard(ModelBase):
    __tablename__ = 'parking_cards'

    blocked = Column(Boolean, nullable=False, default=False)

    subscriptions = relationship("Subscription", backref="parking_cards.id")
