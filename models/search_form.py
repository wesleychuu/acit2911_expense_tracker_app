from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    searched = StringField(
        render_kw={"placeholder": "Search"}, validators=[InputRequired()])
