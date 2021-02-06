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
