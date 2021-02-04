import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [18, 41, 41]  # target percentages; [tie, attacker, defender]
print("1 Infantry (Letnev L4) vs 1 Infantry 1 PDS")

# Units
attacker["infantry"] = 1
defender["infantry"] = 1
defender["pds"] = 1

# Factions
options["att_faction"] = "Letnev"

# Ground Combat
options["ground_combat"] = True

# Options
options["att_letnev_l4_nekro_hide"] = True

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
