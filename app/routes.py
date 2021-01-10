from flask import render_template, redirect
from app import app
import app.calculator as calculator
from app.forms import InputForm
from collections import defaultdict
import requests
import csv
import time


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        attacker = defaultdict(lambda: 0)
        defender = defaultdict(lambda: 0)
        attacker["infantry"] = form.att_inf.data
        defender["infantry"] = form.def_inf.data
        print("form.att_inf.data: %s" % form.att_inf.data)
        print("form.def_inf.data: %s" % form.def_inf.data)
        options = {"ground_combat": True,
                   "att_faction": "Arborec",
                   "def_faction": "Barony"}
        outcomes = calculator.calculate(attacker, defender, options)
        return render_template('index.html', outcomes=outcomes, form=form)

    outcomes = [0, 0, 0]
    return render_template('index.html', outcomes=outcomes, form=form)


# attacker = defaultdict(lambda: 0)
# attacker["flagship"] = 1
# defender = defaultdict(lambda: 0)
# defender["fighter"] = 4
# options = {"ground_combat": False,
#            "att_faction": "Arborec",
#            "def_faction": "Barony"}
# outcomes = calculator.calculate(attacker, defender, options)
