# !/usr/bin/env python

from base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    plate = Column(String(193), unique=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    # TODO: add relation to subscriptions
