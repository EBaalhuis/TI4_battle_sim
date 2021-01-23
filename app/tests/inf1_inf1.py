from collections import defaultdict
import sys, os

sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from app import calculator

# error tolerance in percentage point probability of each outcome
TOL = 1
TARGET = [18, 41, 41]

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

assert(abs(outcomes[0] - TARGET[0]) < TOL)
assert(abs(outcomes[1] - TARGET[1]) < TOL)
assert(abs(outcomes[2] - TARGET[2]) < TOL)

print("Attacker wins: %.1f%%" % outcomes[1])
print("Tie: %.1f%%" % outcomes[0])
print("Defender wins: %.1f%%" % outcomes[2])
file_name = __file__.split("/")[-1]
print("Test " + file_name + " successful")
