import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [18, 41, 41]  # target percentages; [tie, attacker, defender]
print("2 Infantry vs 1 Infantry (Magen Omega)")

# Units
attacker["infantry"] = 2
defender["infantry"] = 1

# Factions

# Ground Combat
options["ground_combat"] = True

# Options
options["def_magen_o"] = True

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
