from app import app, db, scheduler
from app.models import Coin, User
from app.forms import LoginForm, RegistrationForm, EmptyForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from pycoingecko import CoinGeckoAPI
import pprint
import time
from sqlalchemy import desc, asc
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE





# QUERIES AT EVERY INTERVAL
@scheduler.task('interval', id='do_job_1', seconds=300)
def job1():
    with scheduler.app.app_context():
        print("INTERVAL JOB 1 DONE")
        # Get a request from api
        printer = pprint.PrettyPrinter()
        data = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc',
                                    per_page=250,
                                    price_change_percentage='24h,7d')





        
        # Much better request handling
        for i in range(len(data)):
            #printer.pprint(data[i].get('price_change_percentage_7d_in_currency'))
            new_coin = Coin.query.filter_by(name=data[i].get('name')).first()

            if new_coin is None:
                new_coin = Coin(name=data[i].get('name'), symbol=data[i].get('symbol'),
                                current_price=data[i].get('current_price'),
                                market_cap_rank=data[i].get('market_cap_rank'),
                                market_cap=data[i].get('market_cap'),
                                price_change_24h=data[i].get('price_change_percentage_24h'),
                                price_change_7d=data[i].get('price_change_percentage_7d_in_currency'),
                                image=data[i].get('image'))

                print("Added : ", new_coin)
                db.session.add(new_coin)
                db.session.commit()
            else:
                setattr(new_coin, 'current_price', data[i].get('current_price')) 
                setattr(new_coin, 'market_cap_rank',data[i].get('market_cap_rank')) 
                setattr(new_coin, 'market_cap', data[i].get('market_cap'))
                setattr(new_coin, 'price_change_24h',data[i].get('price_change_percentage_24h'))
                setattr(new_coin,'price_change_7d',data[i].get('price_change_percentage_7d_in_currency'))
                db.session.commit()     



# TODO: Need a way to get data for coins into the db
'''
@scheduler.task('interval', id='do_job_2', seconds=70)
def job2():
    with scheduler.app.app_context():
        print("Interval Job 2 Done")
        coin_list = Coin.query.all()
        
        for coin in coin_list:
            filtered_coin_name = coin.name.lower().replace(' ', '')
            historical_data = cg.get_coin_market_chart_by_id(id=filtered_coin_name, 
                                                             vs_currency='usd', days=7,interval='daily')
            print("now sleeping 40 secs")
            time.sleep(40)
            # Store in db then sleep before next iteration
            for times in historical_data:
                setattr(coin,'historical_prices_7d_time',times[0])
                setattr(coin,'historical_prices_7d_prices', times[1]) 
                db.session.commit()
                time.sleep(30)
                print("added {} historical data to db - now sleeping".format(coin.name))


'''

















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
    followed_coins = current_user.followed.order_by(Coin.market_cap_rank.asc()).all()
    if len(followed_coins) == 0:
        flash('You are not following any coins')
    return render_template("profile.html",title="Profile",followed_coins=followed_coins)




@app.route('/coins')
def coins():
    # PAGINATE HERE
    COINS_PER_PAGE = 50 
    page = request.args.get('page', 1, type=int)
    # Sort and Paginate
    printer = pprint.PrettyPrinter()
    coins = Coin.query.order_by(Coin.market_cap_rank.asc()).paginate(page, COINS_PER_PAGE, False)
    return render_template("coin.html", title="Coins",coins=coins)

   
@app.route('/news')
def news():
    return redirect(url_for('index'))


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



# SOME TEST DATA

@app.route('/coins/<int:coin_id>')
def coin_page(coin_id):
    coin_page = Coin.query.filter_by(id=coin_id).first_or_404()
    filtered_coin_name = coin_page.name.lower().replace(' ', '')
    historical_data = cg.get_coin_market_chart_by_id(id=filtered_coin_name, vs_currency='usd',
                                                    days=7,interval='daily')



    historical_data_x = []
    historical_data_y = []
    
    printer = pprint.PrettyPrinter()

    # printer.pprint(historical_data)
    print(type(historical_data))
    for d in historical_data.get('prices'):
        historical_data_x.append(d[0])
        historical_data_y.append(d[1])

    x = historical_data_x
    y = historical_data_y

    fig = figure(plot_width=600, plot_height=600,
                 x_axis_type="datetime")

    fig.line(x,y)


    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    
    script, div = components(fig)
    html = render_template(
        'demo.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources
    )

    # render html here
    html = render_template(
        "coin_page.html", 
        title="{}".format(coin_page.name),
        coin_page=coin_page,
        historical_data=historical_data,
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources)
    
    return html

'''
@app.route('/bokeh')
def bokeh():
    x = historical_data_x
    y = historical_data_y

    fig = figure(plot_width=600, plot_height=600,
                 x_axis_type="datetime")

    fig.line(x,y)


    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    
    script, div = components(fig)
    html = render_template(
        'demo.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources
    )
    return (html)

'''


















