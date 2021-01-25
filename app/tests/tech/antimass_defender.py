import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [9, 54, 37]  # target percentages; [tie, attacker, defender]
print("1 Fighter 1 PDS vs 1 Cruiser (Antimass)")

# Units
attacker["fighter"] = 1
attacker["pds"] = 1
defender["cruiser"] = 1

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["def_antimass"] = True

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
