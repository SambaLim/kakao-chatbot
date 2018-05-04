import os

DIR_PATH = os.path.dirname(__file__)

DEBUG = True

SECRET_KEY = 'lol'

DATABASE_URL = os.environ.get('DATABASE_URL',
    'sqlite:////{0}/requirements.db'.format(DIR_PATH))

SQLALCHEMY_DATABASE_URI = DATABASE_URL


# for GitHub auth
GH_CLIENT_ID = os.environ.get('GH_CLIENT_ID')
GH_CLIENT_SECRET = os.environ.get('GH_CLIENT_SECRET')
