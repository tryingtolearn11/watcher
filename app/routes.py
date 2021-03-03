from app import app
from flask import render_template
from app.forms import LoginForm


@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html", title='Home')



@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", title="Sign in", form=form)



