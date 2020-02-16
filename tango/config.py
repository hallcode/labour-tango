"""
This is the default config for the app, do not change this!

If you wish to customise your installation, add '/tango/instance/config.py' and
write your desired settings there.
"""

import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Static files
STATIC_FOLDER = 'static'
STATIC_URL_PATH = '/static'

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
_session_key = os.environ.get('CSRF_SESSION_KEY')
if not _session_key:
    _session_key = "S35si1on_k3Y--tang1"

CSRF_SESSION_KEY = _session_key

# Secret key for signing cookies
_secret_key = os.environ.get('SECRET_KEY')
if not _secret_key:
    _secret_key = "s£cr3t_K3y--tang02"

SECRET_KEY = _secret_key