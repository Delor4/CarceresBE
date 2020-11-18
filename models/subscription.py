from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import relationship

from classes.ModelBase import ModelBase


class Subscription(ModelBase):
    __tablename__ = 'subscriptions'

    start = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    end = Column(DateTime(timezone=True), nullable=False)
    type = Column(Integer, nullable=False)

    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)

    payment = relationship("Payment", uselist=False, backref="subscriptions.id")
