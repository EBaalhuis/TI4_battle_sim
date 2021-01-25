from flask import render_template, redirect
from app import app
import app.calculator as calculator
from app.route_helpers import units_from_form, options_from_form
from app.forms import InputForm
from collections import defaultdict


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        attacker, defender = units_from_form(form)
        options = options_from_form(form)
        outcomes = calculator.calculate(attacker, defender, options)
        defaults = form
        return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults)
    outcomes = [0, 0, 0]

    defaults = defaultdict(lambda: {"data": "0"})

    return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults, test="att_flagship")


