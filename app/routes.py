from app import app
from flask import render_template, redirect, url_for


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="HOME")








@app.route('/login')
def login():
    return render_template("login.html", title="Login")

