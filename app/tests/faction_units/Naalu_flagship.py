import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [53, 0, 46]  # target percentages; [tie, attacker, defender]
print("1 Flagship 2 Fighter [Naalu] vs 2 Infantry")

# Units
attacker["flagship"] = 1
attacker["fighter"] = 2
defender["infantry"] = 2

# Factions
options["att_faction"] = "Naalu"

# Ground Combat
options["ground_combat"] = True

# Options

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
