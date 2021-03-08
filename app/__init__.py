from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from pycoingecko import CoinGeckoAPI 


app = Flask(__name__)
app.config.from_object(Config)

cg = CoinGeckoAPI()

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models
