import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [13, 29, 58]  # target percentages; [tie, attacker, defender]
print("1 Infantry 1 Dreadnought [Sardakk] vs 3 Infantry")

# Units
attacker["infantry"] = 1
attacker["dread"] = 1
defender["infantry"] = 3

# Factions
options["att_faction"] = "Sardakk"

# Ground Combat
options["ground_combat"] = True

# Options

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
