from app import app
from app.forms import LoginForm
from flask import render_template, redirect, url_for
from pycoingecko import CoinGeckoAPI
import pprint


cg = CoinGeckoAPI()

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="HOME")








@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    return render_template("login.html", title="Login", form=form)




@app.route('/coins')
def coins():
    printer = pprint.PrettyPrinter()
    # Test data
    data = cg.get_price(ids='bitcoin, litecoin, ethereum',vs_currencies='usd,eur')
    

    # Coin ids
    coin_id = cg.get_coins_list()

    coin_names = [i.get('name') for i in coin_id]
    data = coin_names
    


    test22 = cg.get_price(ids='0-5x-long-okb-token', vs_currencies='usd')
    return render_template("coin.html", title="Coins", data=data)



@app.route('/news')
def news():
    return redirect(url_for('index'))
