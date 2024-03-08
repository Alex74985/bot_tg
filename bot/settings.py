import os

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:12345@localhost/flask_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_MAX_OVERFLOW = 4
SECRET_KEY = os.urandom(20)
FLASK_ADMIN_SWATCH = 'cosmo'
BABEL_DEFAULT_LOCALE = 'ru'

