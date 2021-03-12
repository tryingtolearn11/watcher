from app import app, db, scheduler
from app.models import Coin
from app.forms import LoginForm
from flask import render_template, redirect, url_for, flash
from pycoingecko import CoinGeckoAPI
import pprint


@scheduler.task('interval', id='do_job_1', seconds=30)
def job1():
    with scheduler.app.app_context():
        print("INTERVAL JOB DONE")
        # Get a request from api
        printer = pprint.PrettyPrinter()
        data = cg.get_coins_markets(vs_currency='usd')
        #printer.pprint(data) 
        res = []
        for d in data:
            rank = {k: d[k] for k in d.keys() and {'symbol','price_change_24h','name',
                                               'current_price','market_cap_rank','market_cap'}}  
            res.append(rank)
    
        keys = list(res[0].keys())
        # print(keys)


        # TODO: Store data in res[] to db | UPDATE: SOLVED FOR NOW I THINK
        for i in range(len(res)):
            # Find if coin from db exists in our list

            # Find if coin already exists in db
            new_coin = Coin.query.filter_by(name=res[i].get('name')).first() 
            # If not then we add it to db
            if new_coin is None:
                new_coin = Coin(res[i].get('name'), res[i].get('symbol'),
                                res[i].get('current_price'),
                                res[i].get('market_cap_rank'),
                                res[i].get('market_cap'),  res[i].get('price_change_24h'))
                db.session.add(new_coin)
                db.session.commit()
            else:
                # print(new_coin.name, new_coin.current_price)
                # I think it works fine now 
                # UPDATE: TODO: FIX RANKINGS --have to delete old coins or
                # maybe overwrite them 
                # TODO: Need to order the rankings OUT OF ORDER!
                setattr(new_coin, 'name', res[i].get('name')) 
                setattr(new_coin, 'symbol', res[i].get('symbol')) 
                setattr(new_coin, 'current_price', res[i].get('current_price')) 
                setattr(new_coin, 'market_cap_rank',res[i].get('market_cap_rank')) 
                setattr(new_coin, 'market_cap', res[i].get('market_cap'))

                db.session.commit()
        

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


# FOR COMPARISON PURPOSES: btc : current price : 56694 

@app.route('/coins')
def coins():
    # TODO: SORT THE LIST BEFORE SENDING TO CLIENT
    all_coins = Coin.query.all()
    data = cg.get_price(ids='bitcoin',vs_currencies='usd')
    print(data)
    bit = Coin.query.first()
    print(bit)
    '''
    printer = pprint.PrettyPrinter()
    # data = cg.get_coins_markets(vs_currency='usd')
    # printer.pprint(data) 
    # Parse and sort for rank by market cap
    # res = []
    for d in data:
        rank = {k: d[k] for k in d.keys() and {'symbol','price_change_24h','name',
                                               'current_price','market_cap_rank','market_cap'}}  
        res.append(rank)
    keys = list(res[0].keys())
    print(keys)
    # TODO: Store data in res[] to db | UPDATE: SOLVED FOR NOW I THINK
    for i in range(len(res)):
        # Find if coin already exists in db
        new_coin = Coin.query.filter_by(name=res[i].get('name')).first() 
        # If not then we add it to db
        if new_coin is None:
            new_coin = Coin(res[i].get('name'), res[i].get('symbol'),
                            res[i].get('current_price'),
                            res[i].get('market_cap_rank'),
                            res[i].get('market_cap'),  res[i].get('price_change_24h'))
            db.session.add(new_coin)
            db.session.commit()
        else:
            db.session.merge(new_coin)
    '''


    return render_template("coin.html", title="Coins",all_coins=all_coins)



@app.route('/news')
def news():
    return redirect(url_for('index'))
