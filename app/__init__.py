from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.py import login

app = Flask(__name__)
app.secret_key = "you-will-never-guess"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'


db = SQLAlchemy(app)

import routes
