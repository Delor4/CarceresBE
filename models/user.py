#!/usr/bin/env python
from datetime import datetime

from base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy import Integer, String


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(193), unique=True)
    user_type = Column(Integer)
    # TODO: add relation to client (nullable)

    Column('created_on', DateTime(), default=datetime.now)
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)

