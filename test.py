from collections import defaultdict
from app import calculator

attacker = defaultdict(lambda: 0)
attacker["flagship"] = 1
defender = defaultdict(lambda: 0)
defender["fighter"] = 2
defender["pds"] = 4
options = {"ground_combat": False,
           "att_faction": "Argent",
           "def_faction": "Arborec"}
outcomes = calculator.calculate(attacker, defender, options)
print(outcomes)
