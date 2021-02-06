import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [0, 0, 100]  # target percentages; [tie, attacker, defender]
print("1 Dread vs 3 Carrier (Assault)")

# Units
attacker["dread"] = 1
defender["carrier"] = 3

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["def_assault"] = True

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
