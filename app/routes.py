from flask import render_template
from app import app
import app.calculator as calculator
import requests
import csv
import time


@app.route('/')
@app.route('/index')
def index():
    attacker = {"inf": 1}
    defender = {"inf": 1}
    options = {"ground_combat": True}
    outcomes = calculator.calculate(attacker, defender, options)
    return render_template('index.html', outcomes=outcomes)
