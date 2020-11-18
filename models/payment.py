import math

from sqlalchemy import Column, DateTime, Integer, ForeignKey

from classes.ModelBase import ModelBase


class PaidTypes:
    NONE = 0
    DIRECT = 1
    ONLINE = 2


class Payment(ModelBase):
    __tablename__ = 'payments'

    sale_date = Column(DateTime(timezone=True), nullable=False)
    # price in cents
    price = Column(Integer, nullable=False)
    tax = Column(Integer, nullable=False)

    paid_type = Column(Integer, nullable=False, default=PaidTypes.NONE)
    paid_date = Column(DateTime(timezone=True), nullable=True)

    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))

    @property
    def value(self) -> int:
        return int(math.ceil(self.price * (100 + self.tax) / 100))

    @property
    def paid(self):
        if self.paid_type != PaidTypes.NONE and self.paid_date and self.paid_date is not None:
            return True
        return False
