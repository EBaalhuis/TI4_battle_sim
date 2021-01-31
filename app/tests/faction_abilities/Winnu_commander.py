import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/ by comparing to 1 cruiser vs 1 cruiser
target = [25, 38, 38]  # target percentages; [tie, attacker, defender]
print("1 Carrier (Winnu commander) vs 1 Cruiser")

# Units
attacker["carrier"] = 1
defender["cruiser"] = 1

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["att_winnu_commander"] = True

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
