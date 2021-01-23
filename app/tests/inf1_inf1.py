import os
import sys
from collections import defaultdict
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from app import calculator


TOL = 1.5  # error tolerance in percentage point probability of each outcome
TARGET = [18, 41, 41]  # target percentages; [tie, attacker, defender]
attacker = defaultdict(lambda: 0)
defender = defaultdict(lambda: 0)
options = defaultdict(lambda: 0)


# Units
attacker["infantry"] = 1
defender["infantry"] = 1

# Factions
options["att_faction"] = "Winnu"
options["def_faction"] = "Winnu"

# Ground Combat
options["ground_combat"] = True

# Options


outcomes = calculator.calculate(attacker, defender, options)
print("Outcomes:")
print(outcomes)
print("Target:")
print(TARGET)
assert(abs(outcomes[0] - TARGET[0]) < TOL)
assert(abs(outcomes[1] - TARGET[1]) < TOL)
assert(abs(outcomes[2] - TARGET[2]) < TOL)
print("Test successful")
