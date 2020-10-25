import os

from flask import Config


def set_default(cfg, field, val):
    """
    Set default value to field if not present in config.
    """
    if field not in cfg or cfg[field] is None:
        cfg[field] = val


config = Config('./')
config.from_pyfile(os.environ.get("CARCERES_CONFIG", 'settings.py'))

set_default(config, 'SECRET_ACCESS_KEY_EXPIRATION', 600)
set_default(config, 'SECRET_REFRESH_KEY_EXPIRATION', 2592000)

set_default(config, 'AUTOBLOCKADE_ATTEMPTS', 5)
set_default(config, 'AUTOBLOCKADE_TIME', 10)

set_default(config, 'DEFAULT_PAGE_LIMIT', 25)
