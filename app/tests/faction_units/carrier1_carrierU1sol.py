import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [5, 20, 75]  # target percentages; [tie, attacker, defender]
print("1 Carrier vs 1 CarrierU [Sol]")

# Units
attacker["carrier"] = 1
defender["carrier"] = 1
options["def_carrier2"] = True

# Factions
options["def_faction"] = "Sol"

# Ground Combat
options["ground_combat"] = False

# Options

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
