from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager




app = Flask(__name__)
app.config.from_object(Config)
# Database
db = SQLAlchemy(app)

# Migration engine
migrate = Migrate(app, db)

# Login
login = LoginManager(app)



from app import routes, models

