from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Need to create an association table
followers = db.Table('followers',db.Column('user_id', db.Integer, db.ForeignKey('user.id')),db.Column('coin_id', db.Integer, db.ForeignKey('coin.id')))

# UserMixin implements generic properties: is_authenticated, etc
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    followed=db.relationship('Coin',secondary=followers,backref=db.backref('subscribers',lazy='dynamic'),lazy='dynamic')
   
    


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}, followed {} >'.format(self.username,
                                                self.followed.all())
    

    

    def follow(self, coin):
        if not self.is_following(coin):
            self.followed.append(coin)


    def unfollow(self, coin):
        if self.is_following(coin):
            self.followed.remove(coin)

    def is_following(self, coin):
        return self.followed.filter(followers.c.coin_id == coin.id).count() > 0






@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# TODO: Create the db table for coin historical data
# Coin Database Model
class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin_id = db.Column(db.String(64))
    name = db.Column(db.String(64))
    symbol = db.Column(db.String(32))
    current_price = db.Column(db.Float)
    market_cap = db.Column(db.String(180))
    market_cap_rank = db.Column(db.Integer)
    price_change_24h = db.Column(db.Float)
    price_change_7d = db.Column(db.Float)
    image = db.Column(db.String(180))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Get historical data
    historical_prices_7d_time = db.Column(db.String(80))
    historical_prices_7d_prices = db.Column(db.String(100))

    def __init__(self, name, coin_id, symbol, current_price, market_cap_rank,
                 market_cap, price_change_24h, price_change_7d,image):
        self.name = name
        self.coin_id = coin_id
        self.symbol = symbol
        self.current_price = current_price
        self.market_cap_rank = market_cap_rank
        self.market_cap = market_cap
        self.price_change_24h = price_change_24h 
        self.price_change_7d = price_change_7d
        self.image = image
        self.historical_prices_7d_time = historical_prices_7d_time
        self.historical_prices_7d_prices = historical_prices_7d_prices

    def __repr__(self):
        return '<Coin {}, Symbol {}, Price {}, MarketCap Rank {}>'.format(self.name, self.symbol,
                                                       self.current_price, self.market_cap_rank)

