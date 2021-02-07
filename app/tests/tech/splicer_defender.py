import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [2, 49, 49]  # target percentages; [tie, attacker, defender]
print("4 Carrier vs 3 Carrier (Dimensional Splicer)")

# Units
attacker["carrier"] = 4
defender["carrier"] = 3

# Factions
options["def_faction"] = "Nekro"

# Ground Combat
options["ground_combat"] = False

# Options
options["def_creuss_dimensionalsplicer_nekro_hide"] = True

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
