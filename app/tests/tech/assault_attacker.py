import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [2, 49, 49]  # target percentages; [tie, attacker, defender]
print("3 Carrier (Assault Cannon) vs 4 Carrier")

# Units
attacker["carrier"] = 3
defender["carrier"] = 4

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["att_assault"] = True

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
