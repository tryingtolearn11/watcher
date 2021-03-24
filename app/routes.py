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
from bokeh.embed import components, file_html
from bokeh.plotting import figure
from bokeh.resources import INLINE, CDN





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
                new_coin = Coin(name=data[i].get('name'),coin_id=data[i].get('id'),symbol=data[i].get('symbol'),
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

                setattr(new_coin, 'current_price', data[i].get('current_price')) 
                setattr(new_coin, 'market_cap_rank',data[i].get('market_cap_rank')) 
                setattr(new_coin, 'market_cap', data[i].get('market_cap'))
                setattr(new_coin, 'price_change_24h',data[i].get('price_change_percentage_24h'))
                setattr(new_coin,'price_change_7d',data[i].get('price_change_percentage_7d_in_currency'))
                db.session.commit()     



# TODO: Need a way to get data for coins into the db

@scheduler.task('interval', id='do_job_2', seconds=1000)
def job2():
    with scheduler.app.app_context():
        print("Interval Job 2 Done")
        coin_list = Coin.query.all()
        
        for coin in coin_list:
            filtered_coin_name = coin.name.lower().replace(' ', '')
            historical_data = cg.get_coin_market_chart_by_id(id=filtered_coin_name, 
                                                             vs_currency='usd', days=7,interval='daily')
            print("now sleeping 40 secs")
            # Store in db then sleep before next iteration
            for times in historical_data:
                setattr(coin,'historical_prices_7d_time',times[0])
                setattr(coin,'historical_prices_7d_prices', times[1]) 
                db.session.commit()
                print("added {} historical data to db - now sleeping".format(coin.name))
                time.sleep(30)




















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





'''
def profile_plots(followed_coins):
    plots = []
    x = [0, 1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10, 12]
    for i in range(len(followed_coins)):
        p = figure(plot_width=200, plot_height=100, x_axis_type="datetime")
        p.line(x,y)
        plots.append(p)
    return plots
'''





@app.route('/profile')
@login_required
def profile():
    followed_coins = current_user.followed.order_by(Coin.market_cap_rank.asc()).all()
    if len(followed_coins) == 0:
        flash('You are not following any coins')
    
    
    # list to hold all plots
    plots_list = []
    # go through all followed coins
    for i in range(len(followed_coins)):
        coin_page = followed_coins[i]
     #   print(coin_page.coin_id)
        coin_id = coin_page.coin_id
       # historical_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd',
       #                                                  days=7,interval='daily')
    
   # plots = profile_plots(followed_coins)
       
       # plots_list.append(figure(plot_width=200,
       #                         plot_height=100,x_axis_type="datetime"))
    
    plots = {}
    x = [0, 1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10, 12]
    for i in range(len(followed_coins)):
        p = figure(plot_width=200, plot_height=100, x_axis_type="datetime")
        p.line(x,y)
        # Key = Name of Coin and Value  = plot 
        plots['{}'.format(followed_coins[i].name)] = p

    #print(plots)

    script, div = components(plots) 

    #print(div)

    for c in followed_coins:
        if c.name in div:
            print("FOUND :", c.name)


    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    return render_template(
        "profile.html",
        title="Profile",
        followed_coins=followed_coins,
        script=script,
        div=div,
        js_resources=js_resources,
        css_resources=css_resources)



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
    coin_id = coin_page.coin_id
    historical_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd',
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

    fig = figure(plot_width=200, plot_height=100,
                 x_axis_type="datetime")

    fig.line(x,y)
    fig.toolbar_location = None
    fig.toolbar.logo = None

    fig.line(x,y)
        # Customize
    fig.toolbar_location = None
    fig.toolbar.logo = None
        # Grid lines off
    fig.xgrid.grid_line_color = None

    fig.ygrid.grid_line_color = None
        # x y ticks
    fig.xaxis.major_tick_line_color = None
    fig.xaxis.minor_tick_line_color = None

    fig.yaxis.major_tick_line_color = None
    fig.yaxis.minor_tick_line_color = None
        # x  and  y values off 
    fig.xaxis.major_label_text_font_size = '0pt'
    fig.yaxis.major_label_text_font_size = '0pt'

    fig.outline_line_color= None
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    
    script, div = components(fig)

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


















