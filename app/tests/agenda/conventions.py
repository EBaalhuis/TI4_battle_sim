import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [18, 41, 41]  # target percentages; [tie, attacker, defender]
print("1 Infantry 1 Dreadnought vs 1 Infantry - Conventions of War stopping Bombardment")

# Units
attacker["infantry"] = 1
attacker["dread"] = 1
defender["infantry"] = 1

# Factions

# Ground Combat
options["ground_combat"] = True
options["conventions"] = True

# Options

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
