import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [14, 32, 55]  # target percentages; [tie, attacker, defender]
print("1 Fighter vs 1 Fighter [Naalu]")

# Units
attacker["fighter"] = 1
defender["fighter"] = 1

# Factions
options["def_faction"] = "Naalu"

# Ground Combat
options["ground_combat"] = False

# Options

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
