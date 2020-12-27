from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


from classes.config import config

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=create_engine(config["SQLALCHEMY_DATABASE_URI"]),
)
session = scoped_session(Session)
