import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [5, 58, 37]  # target percentages; [tie, attacker, defender]
print("2 Fighter (War Funding) vs 2 Fighter")

# Units
attacker["fighter"] = 2
defender["fighter"] = 2

# Factions
options["att_faction"] = "Winnu"
options["def_faction"] = "Winnu"

# Ground Combat
options["ground_combat"] = False

# Options
options["att_warfunding"] = True

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
