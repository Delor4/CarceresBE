from datetime import datetime

from base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, DateTime


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime(), nullable=False)
    end = Column(DateTime(), nullable=False)
    type = Column(Integer, nullable=False)

    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)

    created_on = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False,)
    updated_on = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
