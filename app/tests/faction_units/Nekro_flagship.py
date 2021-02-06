import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [3, 47, 51]  # target percentages; [tie, attacker, defender]
print("1 Flagship 2 Infantry [Nekro] vs 5 Fighter")

# Units
attacker["flagship"] = 1
attacker["infantry"] = 2
defender["fighter"] = 5

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["att_faction"] = "Nekro"

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
