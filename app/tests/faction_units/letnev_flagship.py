import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [0, 100, 0]  # target percentages; [tie, attacker, defender]
print("1 Flagship [Letnev] vs 1 Fighter")

# Units
attacker["flagship"] = 1
defender["fighter"] = 1

# Factions
options["att_faction"] = "Letnev"

# Ground Combat
options["ground_combat"] = False

# Options

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
