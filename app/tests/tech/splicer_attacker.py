import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [2, 49, 49]  # target percentages; [tie, attacker, defender]
print("3 Carrier (Dimensional Splicer) vs 4 Carrier")

# Units
attacker["carrier"] = 3
defender["carrier"] = 4

# Factions
options["att_faction"] = "Creuss"

# Ground Combat
options["ground_combat"] = False

# Options
options["att_creuss_dimensionalsplicer_nekro_hide"] = True

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
