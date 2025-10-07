from flask_wtf import FlaskForm
from wtforms import SubmitField


class MycrudForm(FlaskForm):
    submit = SubmitField('Save mycrud')
