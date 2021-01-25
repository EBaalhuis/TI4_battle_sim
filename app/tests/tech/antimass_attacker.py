import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [7, 27, 67]  # target percentages; [tie, attacker, defender]
print("1 Fighter (Antimass) vs 1 Fighter 1 PDS")

# Units
attacker["fighter"] = 1
defender["fighter"] = 1
defender["pds"] = 1

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["att_antimass"] = True

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
