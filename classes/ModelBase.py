from datetime import datetime

from sqlalchemy import Column, DateTime

from base import Base


class ModelBase(Base):
    __abstract__ = True

    created_on = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_on = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
