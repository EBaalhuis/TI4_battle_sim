import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [14, 48, 37]  # target percentages; [tie, attacker, defender]
print("1 Dreadnought 1 Fighter vs 1 Dreadnought 1 Fighter (don't risk Direct Hit)")

# Units
attacker["dread"] = 1
attacker["fighter"] = 1
defender["dread"] = 1
defender["fighter"] = 1

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["def_riskdirecthit"] = False

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
