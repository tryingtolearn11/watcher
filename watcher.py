from app import app, db, cache
from app.models import User, Coin, Point


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Coin': Coin, 'Point': Point}
