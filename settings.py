SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///./carceres.db'
BUNDLE_ERRORS = True
DEBUG = True
SECRET_KEY = 'Very secret string. Change this on production!!!'
# in seconds
# 600   = 10 minutes
# 3600  = 1 hour
# 96400 = 1 day
SECRET_KEY_EXPIRATION = 3600

# Alowed failed logins
AUTOBLOCKADE_ATTEMPTS = 5
# Time in minutes
AUTOBLOCKADE_TIME = 10
