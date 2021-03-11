from app import app, db, scheduler
from app.models import Coin
from app.forms import LoginForm
from flask import render_template, redirect, url_for, flash
from pycoingecko import CoinGeckoAPI
import pprint


@scheduler.task('interval', id='do_job_1', seconds=300)
def job1():
    flash('JOB 1 DONE AT {}'.format(seconds))
    print('Job 1 executed')


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
    data = cg.get_coins_markets(vs_currency='usd')
    # printer.pprint(data) 
    # Parse and sort for rank by market cap
    res = []
    for d in data:
        rank = {k: d[k] for k in d.keys() and {'symbol','price_change_24h','name',
                                               'current_price','market_cap_rank','market_cap'}}  
        res.append(rank)
    
    keys = list(res[0].keys())
    print(keys)


    # TODO: Store data in res[] to db
    for i in range(len(res)):
        # Find if coin already exists in db
        new_coin = Coin.query.filter_by(username=res[i].get('name')).first() 
        # If not then we add it to db
        if new_coin is None:
            new_coin = Coin(res[i].get('name'), res[i].get('symbol'),
                            res[i].get('current_price'),
                            res[i].get('market_cap_rank'),
                            res[i].get('market_cap'),  res[i].get('price_change_24h'))
            db.session.add(new_coin)
            db.session.commit()
        else:
            db.session.merge()
        
 





    return render_template("coin.html", title="Coins",res=res)



@app.route('/news')
def news():
    return redirect(url_for('index'))
