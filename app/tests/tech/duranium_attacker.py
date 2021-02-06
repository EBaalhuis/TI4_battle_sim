import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [21, 47, 32]  # target percentages; [tie, attacker, defender]
print("1 Dread (Duranium) vs 1 Dread")

# Units
attacker["dread"] = 1
defender["dread"] = 1

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["att_duranium"] = True

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
