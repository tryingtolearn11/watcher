from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired()])
    password = StringField('Enter Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

