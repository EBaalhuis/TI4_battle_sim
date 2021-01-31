import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/ by comparing to 1 inf vs 2 inf
target = [4, 9, 87]  # target percentages; [tie, attacker, defender]
print("1 Infantry vs 1 Infantry (Sol commander)")

# Units
attacker["infantry"] = 1
defender["infantry"] = 1

# Factions

# Ground Combat
options["ground_combat"] = True

# Options
options["def_sol_commander"] = True

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
