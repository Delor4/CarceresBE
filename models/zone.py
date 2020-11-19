from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from classes.ModelBase import ModelBase


class Zone(ModelBase):
    __tablename__ = 'zones'

    name = Column(String(193), unique=True)
    bkg_file = Column(String(193), nullable=False)
    places = relationship("Place", backref="zones.id", lazy='joined')
