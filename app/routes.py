from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from flask_login import logout_user, current_user, login_user
from app.models import User



@app.route('/')
@app.route('/index')
def index():
    return render_template("home.html", title='Home')



@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is logged in, redirect
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        # load user from db. Query db w/ the username.data from the form to
        # find user. .firt() method returns obj if exists or None. Used to find
        # only 1 result
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        # call login_user(): it registers user logged in and any future pages
        login_user(user, remember=form.username.data)
        return redirect('index')
    return render_template("login.html", title="Sign in", form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
