from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from base import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(193))
    surname = Column(String(193))
    address = Column(String(193))
    city = Column(String(30))
    phone = Column(String(15))

    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=True, default=None)
    user = relationship("User", back_populates="client")

    created_on = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False,)
    updated_on = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    cars = relationship("Car", backref="clients.id", cascade="all, delete")
