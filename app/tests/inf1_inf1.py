import os
import sys
from collections import defaultdict
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from app import calculator

# error tolerance in percentage point probability of each outcome
TOL = 1.5
TARGET = [18, 41, 41]

file_name = __file__.split("/")[-1]
print("Running test " + file_name)

attacker = defaultdict(lambda: 0)
attacker["infantry"] = 1

defender = defaultdict(lambda: 0)
defender["infantry"] = 1

options = defaultdict(lambda: 0)

# Factions
options["att_faction"] = "Winnu"
options["def_faction"] = "Winnu"

# Ground Combat
options["ground_combat"] = True

outcomes = calculator.calculate(attacker, defender, options)

print("Outcomes:")
print(outcomes)
print("Target:")
print(TARGET)
assert(abs(outcomes[0] - TARGET[0]) < TOL)
assert(abs(outcomes[1] - TARGET[1]) < TOL)
assert(abs(outcomes[2] - TARGET[2]) < TOL)
print("Test successful\n")
