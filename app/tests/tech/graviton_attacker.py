import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [7, 24, 69]  # target percentages; [tie, attacker, defender]
print("1 Fighter 1 PDS (Antimass) vs 1 Fighter 1 Cruiser")

# Units
attacker["fighter"] = 1
attacker["pds"] = 1
defender["fighter"] = 1
defender["cruiser"] = 1

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["att_graviton"] = True

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
