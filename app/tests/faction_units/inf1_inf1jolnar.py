import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [14, 55, 32]  # target percentages; [tie, attacker, defender]
print("1 Infantry vs 1 Infantry [Jol-Nar]")

# Units
attacker["infantry"] = 1
defender["infantry"] = 1

# Factions
options["def_faction"] = "Jol-Nar"

# Ground Combat
options["ground_combat"] = True

# Options

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
