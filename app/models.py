from app import db
from datetime import datetime



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))




    def __repr__(self):
        return '<User {}>'.format(self.username)



# Coin Database Model
class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    symbol = db.Column(db.String(32), unique=True)
    current_price = db.Column(db.Float)
    market_cap = db.Column(db.String(180))
    market_cap_rank = db.Column(db.Integer, unique=True)
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
