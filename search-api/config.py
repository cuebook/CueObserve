# Enable Development Env

DEBUG = True

# Application Directory

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# # Example DB Configuration
SQLALCHEMY_DATABASE_URI = f"sqlite:////{BASE_DIR}/db/db.sqlite3"

# SQLALCHEMY_DATABASE_URI = ''
# DATABASE_CONNECT_OPTIONS = {}

# # Application threads. Common assumption is
# # to use 2 threads per available core.
# # Handles incoming requests using one and 
# # performs background operations on other.

# THREADS_PER_PAGE = 2

# # CSRF

# CSRF_ENABLED = True
# CSRF_SESSION_KEY = 'Use http://grc.com/passwords'

# # Key for cookies

# SECRET_KEY = 'Same as Session Key'
