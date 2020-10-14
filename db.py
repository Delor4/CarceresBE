import os

from flask.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

config = Config('./')
config.from_pyfile(os.environ.get("CARCERES_CONFIG", 'settings.py'))

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(config['SQLALCHEMY_DATABASE_URI']))
session = scoped_session(Session)
