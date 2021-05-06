from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from pycoingecko import CoinGeckoAPI 
from sqlalchemy import MetaData
from flask_apscheduler import APScheduler 
from flask_caching import Cache
from flask_bootstrap import Bootstrap
from jinja2 import Markup

app = Flask(__name__)
app.config.from_object(Config)
app.config['CACHE_TYPE'] = 'simple'


login = LoginManager(app)
login.login_view = 'login'
scheduler = APScheduler()
cg = CoinGeckoAPI()
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
bootstrap = Bootstrap(app)
cache = Cache(app)



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
    db.create_all()


































# Filters
def currency_format(price):
    return "${:,.2f}".format(price)

def number_format(number):
    return '{:,}'.format(number)

def percent_color_format(value):
    s = str(value)
    negative = "-"
    if s == "None":
        return " "
    if negative in s:
        return Markup('<span style="color:red"> {} </span>'.format(s[:4]+"%"))
    else:
        return Markup('<span style="color:green"> {} </span>'.format(s[:4]+"%"))

# Jinja2 custom filters
app.jinja_env.filters['currency_format'] = currency_format
app.jinja_env.filters['number_format'] = number_format
app.jinja_env.filters['percent_color_format'] = percent_color_format

from app import routes, models
