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

    Column('created_on', DateTime(), default=datetime.now)
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
