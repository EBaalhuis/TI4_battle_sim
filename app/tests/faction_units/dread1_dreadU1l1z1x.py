import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [29, 26, 45]  # target percentages; [tie, attacker, defender]
print("1 Dreadnought vs 1 DreadnoughtU [L1Z1X]")

# Units
attacker["dread"] = 1
defender["dread"] = 1
options["def_dread2"] = True

# Factions
options["def_faction"] = "L1Z1X"

# Ground Combat
options["ground_combat"] = False

# Options

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
