from sqlalchemy import Column, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from classes.ModelBase import ModelBase


class Payment(ModelBase):
    __tablename__ = 'payments'

    type = Column(Integer, nullable=False)
    paid = Column(Boolean, nullable=False, default=False)
    paid_date = Column(DateTime(timezone=True), nullable=False)

    invoice_id = Column(Integer, ForeignKey("invoices.id"), unique=True, nullable=False)
    invoice = relationship("Invoice", back_populates="payment")
