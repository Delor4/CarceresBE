import math
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from classes.ModelBase import ModelBase


class Invoice(ModelBase):
    __tablename__ = 'invoices'

    sale_date = Column(DateTime(timezone=True), nullable=False)
    # in cents
    price = Column(Integer, nullable=False)
    tax = Column(Integer, nullable=False)
    number = Column(String(20), nullable=False, unique=True)

    subscriptions = relationship("Subscription", backref="invoices.id")
    payment = relationship("Payment", uselist=False, back_populates="invoice")

    @property
    def value(self) -> int:
        return int(math.ceil(self.price * (100 + self.tax)/100))
