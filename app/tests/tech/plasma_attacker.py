import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [3, 86, 11]  # target percentages; [tie, attacker, defender]
print("1 Fighter 1 PDS (Plasma Scoring) vs 1 Fighter")

# Units
attacker["fighter"] = 1
attacker["pds"] = 1
defender["fighter"] = 1

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["att_plasma"] = True

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
