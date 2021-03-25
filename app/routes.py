from flask import render_template, flash
from app import app, html_generator
import app.calculator.calculator as calc
from app.route_helpers import units_from_form, options_from_form, options_list, flash_errors, error_print
from app.forms import InputForm
from collections import defaultdict
import traceback


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        # Get inputs from form
        attacker, defender = units_from_form(form)
        options = options_from_form(form)

        try:
            outcomes = calc.calculate(attacker, defender, options, test=False)
        except:
            error_print(attacker, defender, options)
            flash("Sorry, something went wrong in the calculation :(")
            outcomes = [0, 0, 0]
            traceback.print_exc()

        # Determine which checkboxes should remain checked
        checkboxes = defaultdict(lambda: "")
        for opt in options.keys():
            checkboxes[opt] = "checked" if options[opt] else ""

        # Determine which options should be hidden
        hidden = defaultdict(lambda: False)
        for opt in options.keys():
            if "hide" in opt:
                if "att_" in opt and not options["att_faction"].lower().split("-")[0] in opt:
                    hidden[opt] = True
                if "def_" in opt and not options["def_faction"].lower().split("-")[0] in opt:
                    hidden[opt] = True
        boxes = html_generator.make_boxes(checkboxes, hidden)

        # Remember numbers that were filled in
        defaults = form

        return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults, checkboxes=checkboxes,
                               boxes=boxes)
    else:
        flash_errors(form)

    outcomes = [0, 0, 0]
    defaults = defaultdict(lambda: {"data": "0"})

    checkboxes = defaultdict(lambda: "")
    checkboxes["att_riskdirecthit"] = "checked"
    checkboxes["def_riskdirecthit"] = "checked"

    hidden = defaultdict(lambda: False)
    for opt in options_list():
        if "hide" in opt:
            hidden[opt] = True

    boxes = html_generator.make_boxes(checkboxes, hidden)

    return render_template('index.html', outcomes=outcomes, form=form, defaults=defaults, checkboxes=checkboxes,
                           boxes=boxes)
