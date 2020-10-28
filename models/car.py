from datetime import datetime

from sqlalchemy.orm import relationship

from base import Base
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy import Integer, String


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    plate = Column(String(193), unique=True)
    client_id = Column(Integer, ForeignKey("clients.id"))

    subscriptions = relationship("Subscription", backref="cars.id")

    created_on = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False,)
    updated_on = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
