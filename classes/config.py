import os

from flask import Config

config = Config('./')
config.from_pyfile(os.environ.get("CARCERES_CONFIG", 'settings.py'))
