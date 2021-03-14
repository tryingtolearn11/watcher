from app import app, db, scheduler
from app.models import Coin, User
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from pycoingecko import CoinGeckoAPI
import pprint
from sqlalchemy import desc, asc


# QUERIES AT EVERY INTERVAL
@scheduler.task('interval', id='do_job_1', seconds=20)
def job1():
    with scheduler.app.app_context():
        print("INTERVAL JOB DONE")
        # Get a request from api
        printer = pprint.PrettyPrinter()
        data = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc',
                                    per_page=250, price_change_percentage='24h')
        
        #printer.pprint(data) 
        '''
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
            # Trying to fix the condition for the last coin on the board. It
            # breaks the entire system
            if i == len(res) and new_coin is not None:
                print("removed :", new_coin)
                db.session.delete(new_coin)
                db.session.commit()
                

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
        '''
        # Much better request handling
        for i in range(len(data)):
            # printer.pprint(data[i].get('name'))
            new_coin = Coin.query.filter_by(name=data[i].get('name')).first()
            if new_coin is None:
                new_coin = Coin(name=data[i].get('name'), symbol=data[i].get('symbol'),
                                current_price=data[i].get('current_price'),
                                market_cap_rank=data[i].get('market_cap_rank'),
                                market_cap=data[i].get('market_cap'),
                                price_change_24h=data[i].get('price_change_percentage_24h'),
                                image=data[i].get('image'))

                print("Added : ", new_coin)
                db.session.add(new_coin)
                db.session.commit()
            else:
                setattr(new_coin, 'current_price', data[i].get('current_price')) 
                setattr(new_coin, 'market_cap_rank',data[i].get('market_cap_rank')) 
                setattr(new_coin, 'market_cap', data[i].get('market_cap'))
                setattr(new_coin, 'price_change_24h',data[i].get('price_change_percentage_24h'))
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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
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



@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html",title="Profile")


# Jinja2 custom filter
# TODO: WRITE CUSTOM FILTERS FOR FORMATTING CURRENCY, PERCENTAGES, NUMBERS

# Currency Formatter
def currency_format(price):
    return "${:,.2f}".format(price)


# Number Formatter
def number_format(number):
    return '{:,}'.format(number)



# FILTERS 
app.jinja_env.filters['currency_format'] = currency_format
app.jinja_env.filters['number_format'] = number_format





@app.route('/coins')
def coins():
    # TODO: Maybe we can make a custom filter for jinja and then sort the items
    # in allcoins from coin.html?
    # Or maybe just sort the coins before they get ranked i.e. sort them in
    # this function. 
    # PAGINATE HERE
    COINS_PER_PAGE = 50 
    page = request.args.get('page', 1, type=int)
    coins = Coin.query.paginate(page, COINS_PER_PAGE, False)

    #print(len(all_coins))
    #all_coins.sort(key=lambda x: x.market_cap_rank)
    #for i in range(len(all_coins)-1):
    #   if all_coins[i].market_cap_rank == all_coins[i+1].market_cap_rank:
    #      print(all_coins[i], all_coins[i+1])
    #print(len(all_coins))
    return render_template("coin.html", title="Coins",coins=coins)



@app.route('/news')
def news():
    return redirect(url_for('index'))













