from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    searched = StringField(label="", render_kw={"placeholder": "Search"}, validators=[InputRequired()])
