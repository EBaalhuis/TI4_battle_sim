from collections import defaultdict


def defaults():
    attacker = defaultdict(lambda: 0)
    defender = defaultdict(lambda: 0)
    options = defaultdict(lambda: 0)
    options["att_faction"] = "Winnu"
    options["def_faction"] = "Winnu"
    options["att_riskdirecthit"] = True
    options["def_riskdirecthit"] = True
    tol = 2  # error tolerance in percentage point probability of each outcome

    return attacker, defender, options, tol


def evaluate(outcomes, target, tol):
    print("Outcomes:")
    print(outcomes)
    print("Target:")
    print(target)
    assert (abs(outcomes[0] - target[0]) <= tol)
    assert (abs(outcomes[1] - target[1]) <= tol)
    assert (abs(outcomes[2] - target[2]) <= tol)
    print("Test successful\n")
