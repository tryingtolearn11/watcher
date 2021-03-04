from app.forms import LoginForm
from flask import render_template, redirect, url_for


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="HOME")








@app.route('/login', methods = ['GET', 'POST'])
def login():
    form=LoginForm()
    return render_template("login.html", title="Login")

