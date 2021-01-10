from flask import render_template
from app import app
import app.calculator as calculator
from collections import defaultdict
import requests
import csv
import time


@app.route('/')
@app.route('/index')
def index():
    attacker = defaultdict(lambda: 0)
    attacker["flagship"] = 1
    defender = defaultdict(lambda: 0)
    defender["fighter"] = 4
    options = {"ground_combat": False,
               "att_faction": "Arborec",
               "def_faction": "Barony"}
    outcomes = calculator.calculate(attacker, defender, options)
    return render_template('index.html', outcomes=outcomes)


attacker = defaultdict(lambda: 0)
attacker["flagship"] = 1
defender = defaultdict(lambda: 0)
defender["fighter"] = 4
options = {"ground_combat": False,
           "att_faction": "Arborec",
           "def_faction": "Barony"}
outcomes = calculator.calculate(attacker, defender, options)
