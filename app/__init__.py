from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from pycoingecko import CoinGeckoAPI 
from sqlalchemy import MetaData
from flask_apscheduler import APScheduler 
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
app.config.from_object(Config)


scheduler = APScheduler()
cg = CoinGeckoAPI()
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
bootstrap = Bootstrap(app)
naming_convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

scheduler.init_app(app)
scheduler.start()

with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app,db)




from app import routes, models
