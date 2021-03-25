import random


def roll():
    # Simulate rolling a 10-sided die, return random int between 1 and 10 (inclusive) uniformly
    x = random.random()
    return int(x * 10 + 1)


def has_flagship(units):
    return any(map(lambda u: u.name == "flagship", units))


def has_mech(units):
    return any(map(lambda u: u.name == "mech", units))


def above_average(units, hits):
    # determine whether this number of hits was above the expected amount for this set of units
    expected = 0
    for u in units:
        for val in u.combat:
            expected += min(1, 1 - 0.1 * (val - 1))

    return hits > expected
