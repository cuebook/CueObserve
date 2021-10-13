import os

# Enable Development Env
DEBUG = True

# Application Directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# # Example DB Configuration
if os.environ.get("SEARCH_POSTGRES_DB_HOST", None):
    POSTGRES_DB_NAME = os.environ.get("SEARCH_POSTGRES_DB_SCHEMA")
    POSTGRES_DB_USER = os.environ.get("SEARCH_POSTGRES_DB_USERNAME")
    POSTGRES_DB_PASSWORD = os.environ.get("SEARCH_POSTGRES_DB_PASSWORD")
    POSTGRES_DB_HOST = os.environ.get("SEARCH_POSTGRES_DB_HOST")
    POSTGRES_DB_PORT = os.environ.get("SEARCH_POSTGRES_DB_PORT")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_DB_USER}:{POSTGRES_DB_PASSWORD}@{POSTGRES_DB_HOST}:{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}"
else:
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{BASE_DIR}/db/db.sqlite3"

DATASET_URL = os.environ.get("DATASET_URL", "http://localhost:8000/api/dataset/data/")

# DATABASE_CONNECT_OPTIONS = {}
DIMENSION_URL = os.environ.get("DIMENSION_URL", "http://localhost:8000/api/anomaly/search/dimension/")
METRIC_URL = os.environ.get("METRIC_URL", "http://localhost:8000/api/anomaly/search/metrics/")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200/")
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
