import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [40, 60, 0]  # target percentages; [tie, attacker, defender]
print("1 Flagship 1 Fighter [Yin] vs 3 Fighter")

# Units
attacker["flagship"] = 1
attacker["fighter"] = 1
defender["fighter"] = 3

# Factions
options["att_faction"] = "Yin"

# Ground Combat
options["ground_combat"] = False

# Options

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
