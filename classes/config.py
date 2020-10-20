import os

from flask import Config

def set_default(conf, field, val):
    if not conf[field] or conf[field] is None:
        conf[field] = val

config = Config('./')
config.from_pyfile(os.environ.get("CARCERES_CONFIG", 'settings.py'))

set_default(config, 'SECRET_KEY_EXPIRATION', 600)

set_default(config, 'AUTOBLOCKADE_ATTEMPTS', 5)
set_default(config, 'AUTOBLOCKADE_TIME', 10)
