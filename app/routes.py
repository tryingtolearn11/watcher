from app import app
from app.forms import LoginForm
from flask import render_template, redirect, url_for
from pycoingecko import CoinGeckoAPI
import pprint

# pycoingecko
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
    coin_id = cg.get_coins_list()
    # Test data
    # data = cg.get_price(ids='bitcoin, litecoin, ethereum',vs_currencies='usd,eur')

    # Coin ids

   
    data = cg.get_coins_markets(vs_currency='usd')
   # printer.pprint(data)
    

    for d in data:
        res = {k: d[k] for k in d.keys() and {'name','market_cap_rank'}}
        print(str(res))

       # for category in categories:
            #print('CATEGORY:', category)








    return render_template("coin.html", title="Coins", data=data)



@app.route('/news')
def news():
    return redirect(url_for('index'))
