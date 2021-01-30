from flask import render_template, redirect
from app import app
import app.calculator as calculator
from app.route_helpers import units_from_form, options_from_form
from app.forms import InputForm
from collections import defaultdict
import html_generator


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        attacker, defender = units_from_form(form)
        options = options_from_form(form)
        outcomes = calculator.calculate(attacker, defender, options)
        defaults = form

        checkboxes = defaultdict(lambda x: "")
        for opt in options.keys():
            checkboxes[opt] = "checked" if options[opt] else ""

        return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults, checkboxes=checkboxes)
    outcomes = [0, 0, 0]

    defaults = defaultdict(lambda: {"data": "0"})
    checkboxes = defaultdict(lambda x: "")
    checkboxes["att_riskdirecthit"] = "checked"
    checkboxes["def_riskdirecthit"] = "checked"

    boxes = html_generator.make_boxes()

    return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults, checkboxes=checkboxes,
                           boxes=boxes)


