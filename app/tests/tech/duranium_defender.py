import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [21, 32, 47]  # target percentages; [tie, attacker, defender]
print("1 Dread (Duranium) vs 1 Dread")

# Units
attacker["dread"] = 1
defender["dread"] = 1

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["def_duranium"] = True

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
