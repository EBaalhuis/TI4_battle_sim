from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField


class InputForm(FlaskForm):
    att_inf = IntegerField("Attacker infantry", default=0)
    def_inf = IntegerField("Defender infantry", default=0)
    submit = SubmitField("Calculate")
