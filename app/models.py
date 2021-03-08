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
    current_price = db.Column(db.Float)
    market_cap = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Coin {}, Price {}, Market Cap {}, Time {}>,'.format(self.name,self.current_price, self.market_cap, self.timestamp)
