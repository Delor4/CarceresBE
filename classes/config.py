import os

from flask import Flask

flask_app = Flask(__name__)

flask_app.config.from_object('settings')

CARCERES_CONFIG = os.environ.get("CARCERES_CONFIG")

if CARCERES_CONFIG:
    flask_app.config.from_envvar('CARCERES_CONFIG')
