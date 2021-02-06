import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
import app.calculator.calculator as calc
from app import testing_helpers


attacker, defender, options, tol = testing_helpers.defaults()

# target source: http://alphamou.se/ti4calc/
target = [11, 61, 28]  # target percentages; [tie, attacker, defender]
print("4 Fighters vs 1 War Sun - Publicize Weapon Schematics makes War Sun lose Sustain Damage")

# Units
attacker["fighter"] = 4
defender["warsun"] = 1

# Factions

# Ground Combat
options["ground_combat"] = False
options["publicize"] = True

# Options

outcomes = calc.calculate(attacker, defender, options)
testing_helpers.evaluate(outcomes, target, tol)
