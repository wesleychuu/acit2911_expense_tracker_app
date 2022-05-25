from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo


class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[InputRequired(), Length(min=8, max=80)])
    new_password = PasswordField('New Password', validators=[
                             InputRequired(),
                             Length(min=8, max=80),
                             Regexp('(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)',
                                    message="Passwords must be 8 characters long with at least one uppercase character, one lowercase character, one number, and one special character."),
                             EqualTo('confirm', message="Passwords must match")
                             ]
                            )
    confirm = PasswordField('Confirm Password')