from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config



app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'


db = SQLAlchemy(app)

from app import routes
