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
        options["att_faction"] = "Sardakk"
        options["def_faction"] = "Letnev"
        outcomes = calculator.calculate(attacker, defender, options)
        defaults = form
        return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults)

    outcomes = [0, 0, 0]
    defaults = defaultdict(lambda: {"data": "0"})
    defaults["ground_combat"] = False
    return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults, test="att_flagship")


# attacker = defaultdict(lambda: 0)
# attacker["flagship"] = ""
# defender = defaultdict(lambda: 0)
# defender["fighter"] = 4
# options = {"ground_combat": False,
#            "att_faction": "Arborec",
#            "def_faction": "Barony"}
# outcomes = calculator.calculate(attacker, defender, options)
# print(outcomes)
