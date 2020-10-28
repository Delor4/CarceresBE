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
    user_type = Column(Integer) # see classes.auth.Rights
    password_hash = Column(String(128))
    failed_logins = Column(Integer, default=0, nullable=False)
    blocked_since = Column(DateTime, nullable=True)

    client = relationship("Client", uselist=False, back_populates="user")

    created_on = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False,)
    updated_on = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def hash_password(self, password):
        """
        Hash given password.
        """
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """
        Check if user's hashed password and given password match.
        """
        return pwd_context.verify(password, self.password_hash)
