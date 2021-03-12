from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# UserMixin implements generic properties: is_authenticated, etc
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))




# Coin Database Model
class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    symbol = db.Column(db.String(32))
    current_price = db.Column(db.Float)
    market_cap = db.Column(db.String(180))
    market_cap_rank = db.Column(db.Integer)
    price_change_24h = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    

    def __init__(self, name, symbol, current_price, market_cap_rank,
                 market_cap, price_change_24h):
        self.name = name
        self.symbol = symbol
        self.current_price = current_price
        self.market_cap_rank = market_cap_rank
        self.market_cap = market_cap
        self.price_change_24h = price_change_24h 
    def __repr__(self):
        return '<Coin {}, Symbol {}, Price {}>'.format(self.name, self.symbol,
                                                       self.current_price)
       # return '<Coin {}, Price {}, Market Cap {}, Time
       # {}>,'.format(self.name,self.current_price, self.market_cap, self.#timestamp)
