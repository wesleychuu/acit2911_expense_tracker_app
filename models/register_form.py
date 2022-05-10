from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, Regexp


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[
                       InputRequired(), Length(min=4, max=50)])
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=30)])
    email = StringField('Email', validators=[InputRequired(), Email(
        message="Invalid email"), Length(max=50)])
    password = PasswordField('Password', validators=[
                             InputRequired(),
                             Length(min=8, max=80),
                             Regexp('(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)',
                                    message="Passwords must be 8 characters long with at least one uppercase character, one lowercase character, and one special character.")
                             ])
