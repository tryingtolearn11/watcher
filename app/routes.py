from app import app
from app.forms import LoginForm
from flask import render_template, redirect, url_for
from pycoingecko import CoinGeckoAPI


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="HOME")








@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    return render_template("login.html", title="Login", form=form)




cg = CoinGeckoAPI()
@app.route('/coins')
def coins():
    data = cg.get_price(ids='bitcoin, litecoin, ethereum',
                        vs_currencies='usd,eur')
    print(data)
    return render_template("coin.html", title="Coins", data=data)



@app.route('/news')
def news():
    return redirect(url_for('index'))
