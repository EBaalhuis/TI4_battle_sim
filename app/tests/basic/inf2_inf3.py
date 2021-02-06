import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [3, 16, 81]  # target percentages; [tie, attacker, defender]
print("2 Infantry vs 3 Infantry")

# Units
attacker["infantry"] = 2
defender["infantry"] = 3

# Factions

# Ground Combat
options["ground_combat"] = True

# Options

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
