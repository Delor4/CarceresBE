#!/usr/bin/env python
from datetime import datetime

from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship

from base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(193), unique=True)
    user_type = Column(Integer)
    password_hash = Column(String(128))
    failed_logins = Column(Integer, default=0, nullable=False)
    blocked_since = Column(DateTime, nullable=True)

    client = relationship("Client", uselist=False, back_populates="user")

    Column('created_on', DateTime(), default=datetime.now)
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
