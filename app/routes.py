from flask import render_template
from app import app, html_generator
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

        checkboxes = defaultdict(lambda: "")
        for opt in options.keys():
            checkboxes[opt] = "checked" if options[opt] else ""

        boxes = html_generator.make_boxes(checkboxes)

        return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults, checkboxes=checkboxes,
                               boxes=boxes)

    outcomes = [0, 0, 0]
    defaults = defaultdict(lambda: {"data": "0"})
    checkboxes = defaultdict(lambda: "")
    checkboxes["att_riskdirecthit"] = "checked"
    checkboxes["def_riskdirecthit"] = "checked"

    boxes = html_generator.make_boxes(checkboxes)

    return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults, checkboxes=checkboxes,
                           boxes=boxes)
