import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from app import calculator
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [14, 37, 48]  # target percentages; [tie, attacker, defender]
print("1 Dreadnought 1 Fighter (don't risk Direct Hit) vs 1 Dreadnought 1 Fighter")

# Units
attacker["dread"] = 1
attacker["fighter"] = 1
defender["dread"] = 1
defender["fighter"] = 1

# Factions

# Ground Combat
options["ground_combat"] = False

# Options
options["att_riskdirecthit"] = False

outcomes = calculator.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
