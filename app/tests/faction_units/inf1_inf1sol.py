import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [21, 31, 48]  # target percentages; [tie, attacker, defender]
print("1 Infantry vs 1 Infantry [Sol]")

# Units
attacker["infantry"] = 1
defender["infantry"] = 1

# Factions
options["def_faction"] = "Sol"

# Ground Combat
options["ground_combat"] = True

# Options

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
