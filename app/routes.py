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
        print(form["att_antimass"])
        print(form["def_antimass"])
        print(options["att_antimass"])
        print(options["def_antimass"])
        print(form["att_graviton"])
        print(form["def_graviton"])
        print(options["att_graviton"])
        print(options["def_graviton"])
        outcomes = calculator.calculate(attacker, defender, options)
        defaults = form
        return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults)
    outcomes = [0, 0, 0]

    defaults = defaultdict(lambda: {"data": "0"})
    labels = ["ground_combat", "att_faction", "def_faction", "att_antimass", "def_antimass", "att_graviton",
              "def_graviton", "att_plasma", "def_plasma", "def_magen", "def_magen_o", "att_bacterial", "att_duranium",
              "def_duranium", "att_assault", "def_assault"]
    for label in labels:
        defaults[label] = False

    return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults, test="att_flagship")


