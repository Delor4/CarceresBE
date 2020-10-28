from datetime import datetime

from base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime
from sqlalchemy import Integer, String


class Zone(Base):
    __tablename__ = 'zones'

    id = Column(Integer, primary_key=True)
    name = Column(String(193), unique=True)
    bkg_file = Column(String(193), nullable=False)
    places = relationship("Place", backref="zones.id")

    created_on = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False,)
    updated_on = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
