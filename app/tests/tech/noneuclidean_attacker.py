import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [9, 69, 22]  # target percentages; [tie, attacker, defender]
print("2 Dread (Non-Euclidean Shielding) vs 2 Dread")

# Units
attacker["dread"] = 2
defender["dread"] = 2

# Factions
options["att_faction"] = "Letnev"

# Ground Combat
options["ground_combat"] = False

# Options
options["att_letnev_noneuclidean_nekro_hide"] = True

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
