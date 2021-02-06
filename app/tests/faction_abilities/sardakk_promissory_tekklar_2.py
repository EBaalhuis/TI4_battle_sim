import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [21, 48, 31]  # target percentages; [tie, attacker, defender]
print("1 Infantry vs 1 Infantry")

# Units
attacker["infantry"] = 1
defender["infantry"] = 1

# Factions

# Ground Combat
options["ground_combat"] = True

# Options
options["att_tekklar"] = True
options["def_faction"] = "Sardakk"

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
