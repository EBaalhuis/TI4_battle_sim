import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [11, 36, 54]  # target percentages; [tie, attacker, defender]
print("1 Cruiser 1 Destroyer [Mentak] vs 2 Cruiser [Mentak]")

# Units
attacker["cruiser"] = 1
attacker["destroyer"] = 1
defender["cruiser"] = 2

# Factions
options["att_faction"] = "Mentak"
options["def_faction"] = "Mentak"

# Ground Combat
options["ground_combat"] = False

# Options

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
