import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'optional')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_ENABLED = True
    CACHE_TYPE = 'simple' 
