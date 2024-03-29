from app import app, db, scheduler, cache
from app.models import Coin, User, Point
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash, request
from flask_caching import Cache
from werkzeug.urls import url_parse
from pycoingecko import CoinGeckoAPI
import pprint
import time
from sqlalchemy import desc, asc
from bokeh.embed import components, file_html
from bokeh.plotting import figure
from bokeh.resources import INLINE, CDN
from bokeh.models import NumeralTickFormatter


# pycoingecko
cg = CoinGeckoAPI()


# QUERIES AT EVERY INTERVAL
@scheduler.task('interval', id='do_job_1', seconds=1500)
def job1():
    with scheduler.app.app_context():
        try:
            print("INTERVAL JOB 1 DONE")
            # Get a request from api
            data = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc',
                                        per_page=250,
                                        price_change_percentage='24h,7d')



            # Much better request handling
            for i in range(len(data)):
                new_coin = Coin.query.filter_by(name=data[i].get('name')).first()
                
                # If coin is new, add to db
                if new_coin is None:
                    new_coin = Coin(name=data[i].get('name'), coin_id=data[i].get('id'),symbol=data[i].get('symbol'),
                                    current_price=data[i].get('current_price'),
                                    market_cap_rank=data[i].get('market_cap_rank'),
                                    market_cap=data[i].get('market_cap'),
                                    price_change_24h=data[i].get('price_change_percentage_24h'),
                                    price_change_7d=data[i].get('price_change_percentage_7d_in_currency'),
                                    image=data[i].get('image'))

                    print("Added : ", new_coin)
                    print("{}".format(new_coin.coin_id))
                    db.session.add(new_coin)
                    db.session.commit()

                else:

                    # Otherwise update the numbers for coins
                    setattr(new_coin, 'current_price', data[i].get('current_price')) 
                    setattr(new_coin, 'market_cap_rank',data[i].get('market_cap_rank')) 
                    setattr(new_coin, 'market_cap', data[i].get('market_cap'))
                    setattr(new_coin, 'price_change_24h',data[i].get('price_change_percentage_24h'))
                    setattr(new_coin,'price_change_7d',data[i].get('price_change_percentage_7d_in_currency'))
                    db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            failed=True



# Queries for historical data per coin
@scheduler.task('interval', id='do_job_2', seconds=4000)
def job2():
    with scheduler.app.app_context():
        # Get data from our db
        list = Coin.query.order_by(Coin.market_cap_rank.asc()).all()
        coins = list
        # keep track at index of coin
        count = 0
        for coin in coins[0:100]:
            print(coin.name)
            # Get data from request
            historical_data = cg.get_coin_market_chart_by_id(id=coin.coin_id,
                                                                   vs_currency='usd',
                                                                   days=7,
                                                                   interval='daily')

            # Now filter data into x and y lists 
            x = [t[0] for t in historical_data.get('prices')]
            y = [p[1] for p in historical_data.get('prices')]
    
            data = coin.data.all()
            for k in range(len(x)):
                if len(data) == 0:
                    p = Point(x=x[k], y=y[k], parent=coin)
                    db.session.add(p)
                
                # If Coin already has existing data
                else:
                    if len(data) == len(x):
                    # If this "time" is not in our db
                        if x[k] not in data and len(x) >= 168:
                            setattr(data[k], 'x', str(x[k-1]))
                            setattr(data[k], 'y', str(y[k-1]))
                
            
            count+=1
            db.session.commit()
            print('{} data was added'.format(coin.name))
            print("Coin # : ", count)
            print("NOW SLEEPING")
            time.sleep(3)

        print("JOB2 All done :) ")


                
# Clean DB
# TODO: SCHEDULE A PROPER DB CLEANUP 
@scheduler.task('interval', id='do_job_3', seconds=72000)
def job3():
    with scheduler.app.app_context():
        print("INTERVAL JOB 3 DONE")
        # Sort by oldest to newest
        coins = Coin.query.order_by(Coin.timestamp.desc()).all()
        for k in range((len(coins))):
            # print("deleted {}".format(coin[k].id))
            data = coin[k].data.all()
            for p in data:
                db.session.delete(p)
            db.session.delete(coin[k])
        db.session.commit()





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



# PLOTTING FUNCTION 
def plot(coins):

    all_x_data = {}    
    all_y_data = {}    
    
    # store plots in dict 
    plots = {}
    # go through all followed coins
    for i in range(len(coins)):
        coin = coins[i]
        # Get the historical date by coin id from db
        data = coin.data.order_by(Point.x.asc()).all()
        x = [int(i.x) for i in data]
        y = [float(j.y) for j in data]

        # Store seperated data by name and by x/y axis
        all_x_data[coin.name] = x
        all_y_data[coin.name] = y


        times = all_x_data.get(coin.name)
        prices = all_y_data.get(coin.name)

        # Plot data
        p = figure(plot_width=200, plot_height=100, x_axis_type="datetime")
        p.line(times,prices)

        # Clean up the graph - remove excess info
        p.toolbar_location = None
        p.toolbar.logo = None

        # Customize
        p.toolbar_location = None
        p.toolbar.logo = None

        # Grid lines off
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None

        # x y ticks
        p.xaxis.major_tick_line_color = None
        p.xaxis.minor_tick_line_color = None
        p.yaxis.major_tick_line_color = None
        p.yaxis.minor_tick_line_color = None

        # x  and  y values off 
        p.xaxis.major_label_text_font_size = '0pt'
        p.yaxis.major_label_text_font_size = '0pt'

        p.outline_line_color= None


        # Key = Name of Coin and Value  = plot 
        plots[coins[i].name] = p

    if len(plots) != 0:
        script, div = components(plots)

    # Condition for no coins
    else:
        script = ""
        div = ""
        
    return script, div


@app.route('/profile')
@login_required
def profile():
    followed_coins = current_user.followed.order_by(Coin.market_cap_rank.asc()).all()
    if len(followed_coins) == 0:
        flash('You are not following any coins')
    
    # Plot 
    script, div = plot(followed_coins)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
        
    for c in followed_coins:
        if c.name in div:
            print("FOUND :", c.name)


    return render_template(
        "profile.html",
        title="Profile",
        followed_coins=followed_coins,
        script=script,
        div=div,
        js_resources=js_resources,
        css_resources=css_resources)


# MIGHT HAVE TO CACHE ON THE HTML FILE INSTEAD OF HERE
@app.route('/coins')
# @cache.cached(timeout=300)
def coins():
    # PAGINATE HERE
    COINS_PER_PAGE = 25 
    page = request.args.get('page', 1, type=int)
    # Sort and Paginate
    coins =Coin.query.order_by(Coin.market_cap_rank.asc()).paginate(page,COINS_PER_PAGE,False)
    all_coins = coins.items

    # Plot
    script, div = plot(all_coins)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    return render_template(
        "coin.html",
        title="Coins",
        coins=coins,
        all_coins=all_coins,
        script=script,
        div=div,
        js_resources=js_resources,
        css_resources=css_resources)


# Follow coins/ unfollow
@app.route('/follow/<int:coin_id>/<action>')
@login_required
def follow(coin_id, action):
    coin = Coin.query.filter_by(id=coin_id).first_or_404()
    print(coin)
    if action == "follow":
        current_user.follow(coin)
        flash('You are following {}'.format(coin.name))
        db.session.commit()
    elif action == "unfollow":
        current_user.unfollow(coin)
        flash('You unfollowed {}'.format(coin.name))
        db.session.commit()
        
    return redirect(request.referrer)




@app.route('/coins/<int:coin_id>')
def coin_page(coin_id):
    coin_page = Coin.query.filter_by(id=coin_id).first_or_404()
    coin_id = coin_page.coin_id
    print(coin_id)
    
    data = coin_page.data.order_by(Point.x.asc()).all()
    print("length of data : ", len(data))

    # Checking for duplicate times
    for i in range(len(data)):
        if data[i].x == data[~i].x:
            print(data[i], data[~i])
        
    # Plotting 
    times = [int(i.x) for i in data]
    print("x : ", len(times))
    prices = [float(j.y) for j in data]
    
    p = figure(plot_width=600, plot_height=500,
                 x_axis_type="datetime")

    
    p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
    p.line(times, prices)

    # Customize
    p.toolbar_location = None
    p.toolbar.logo = None

    # Grid lines off
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    
    script, div = components(p)

    # render html here
    html = render_template(
        "coin_page.html", 
        title="{}".format(coin_page.name),
        coin_page=coin_page,
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources)
    
    return html


@app.route('/about')
def about():
    return render_template('about.html', title='About')











