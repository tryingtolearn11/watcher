from app import app, db, scheduler
from app.models import Coin, User
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, flash
from pycoingecko import CoinGeckoAPI
import pprint

# QUERIES AT EVERY INTERVAL
@scheduler.task('interval', id='do_job_1', seconds=10)
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

        # TODO: RANK BUG: DUPLICATE RANKS 
        for i in range(len(res)):
            new_coin = Coin.query.filter_by(name=res[i].get('name')).first() 
            if new_coin is None:
                new_coin = Coin(res[i].get('name'), res[i].get('symbol'),
                                res[i].get('current_price'),
                                res[i].get('market_cap_rank'),
                                res[i].get('market_cap'),  res[i].get('price_change_24h'))
                print("Added : ", new_coin)
                db.session.add(new_coin)
                db.session.commit()

            else:
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
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect('/login')
        login_user(user, remember = form.remember_me.data)
        return redirect(url_for('index'))
    return render_template("login.html", title="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you have registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/coins')
def coins():
    
    # Sort the data before leaderboard
    all_coins = Coin.query.order_by(Coin.market_cap_rank.asc()).all() 
    print(len(all_coins))
    # TODO: Come up with a better solution to fix this issue
    # ISSUE: multiple coins all ranked at 100 at the bottom of list
    # To ensure we only keep the 100 coins in our list
    # I will remove the extra coins. 






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






































