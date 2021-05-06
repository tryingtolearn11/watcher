import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'optional')
    SQLALCHEMY_DATABASE_URI = ("postgres://tyvcokngtzbgwk:c3c3c7f9057dc4d29519b6d90082bc93afc9acfe657df1f26e63e14eb516d512@ec2-107-22-83-3.compute-1.amazonaws.com:5432/d2c4t9516v697d")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_ENABLED = True
    CACHE_TYPE = 'simple' 
