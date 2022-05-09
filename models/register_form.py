from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[
                       InputRequired(), Length(min=4, max=50)])
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=30)])
    email = StringField('email', validators=[InputRequired(), Email(
        message="Invalid email"), Length(max=50)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])
