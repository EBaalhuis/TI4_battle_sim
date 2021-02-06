import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [0, 60, 40]  # target percentages; [tie, attacker, defender]
print("1 Infantry 1 Dread (X89) vs 5 Infantry")

# Units
attacker["infantry"] = 1
attacker["dread"] = 1
defender["infantry"] = 5

# Factions

# Ground Combat
options["ground_combat"] = True

# Options
options["att_x89"] = True

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
