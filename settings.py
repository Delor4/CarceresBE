SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///./carceres.db'
# Sample URI for mysql database
# SQLALCHEMY_DATABASE_URI = 'mysql://<user>:<password>@<host>/<database>'

BUNDLE_ERRORS = True

DEBUG = True
SECRET_KEY = 'Very secret string. Change this on production!!!'

# in seconds
# 600   = 10 minutes
# 3600  = 1 hour
# 86400 = 1 day
# 2592000 = 30 days
# 15768000 = half year
SECRET_ACCESS_KEY_EXPIRATION = 3600
SECRET_REFRESH_KEY_EXPIRATION = 2592000

# Allowed failed logins
AUTOBLOCKADE_ATTEMPTS = 5
# Time in minutes
AUTOBLOCKADE_TIME = 10

# DEFAULT_PAGE_LIMIT = 50
