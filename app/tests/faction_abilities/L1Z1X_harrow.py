import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [11, 62, 26]  # target percentages; [tie, attacker, defender]
print("1 Dreadnought 2 Infantry [L1Z1X] vs 3 Infantry\nTesting Harrow")

# Units
attacker["dread"] = 1
attacker["infantry"] = 2
defender["infantry"] = 3

# Factions
options["att_faction"] = "L1Z1X"

# Ground Combat
options["ground_combat"] = True

# Options

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
