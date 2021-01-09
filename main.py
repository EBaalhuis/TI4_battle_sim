import random
import copy
import units


def generate_hits(units):
    result = 0
    for u in units:
        x = random.randint(1, 10)
        if x >= u.combat:
            result += 1
    return result


def assign_hits(units, hits):
    for u in units:
        if hits == 0:
            return units
        if u.sustain:
            u.sustain = False
            hits -= 1

    while hits > 0 and units:
        del units[0]
        hits -= 1

    return units


def combat_round(att_units, def_units):
    att_hits = generate_hits(att_units)
    def_hits = generate_hits(def_units)

    att_units = assign_hits(att_units, def_hits)
    def_units = assign_hits(def_units, att_hits)

    return att_units, def_units


def bombardment(units):
    result = 0
    for u in units:
        if u.bombard:
            x = random.randint(1, 10)
            if x >= u.bombard:
                result += 1
    return result


def iteration(att_units, def_units, ground_combat):
    # 0 - tie
    # 1 - attacker won
    # 2 - defender won

    # bombardment
    if ground_combat:
        bombard_hits = bombardment(att_units)
        def_units = assign_hits(def_units, bombard_hits)

    while att_units and def_units:
        att_units, def_units = combat_round(att_units, def_units)

    if not att_units and not def_units:
        return 0
    elif not att_units:
        return 2
    elif not def_units:
        return 1


def filter_ground(units):
    result = []
    for u in units:
        if u.ground:
            result.append(u)
        elif u.bombard:
            u.combat = 99  # disable combat
            result.append(u)
    return result


def filter_space(units):
    return list(filter(lambda x: not x.ground, units))


def run_simulation(att_units, def_units, it=10000, ground_combat=False):
    outcomes = [0, 0, 0]

    if ground_combat:
        att_units = filter_ground(att_units)
        def_units = filter_ground(def_units)
    else:
        att_units = filter_space(att_units)
        def_units = filter_space(def_units)

    for i in range(it):
        res = iteration(copy.deepcopy(att_units), copy.deepcopy(def_units), ground_combat)
        outcomes[res] += 1

    return outcomes


def print_results(outcomes, it=10000):
    print("Attacker wins: %.1f%%" % (outcomes[1] / it * 100))
    print("Tie: %.1f%%" % (outcomes[0] / it * 100))
    print("Defender wins: %.1f%%" % (outcomes[2] / it * 100))


att_inf = 2
att_dreads = 0
def_mech = 0
def_inf = 2
att_units = [units.infantry()] * att_inf + [units.dread()] * att_dreads
def_units = [units.infantry()] * def_inf + [units.mech()] * def_mech

outcomes = run_simulation(att_units, def_units, ground_combat=True)

print_results(outcomes)
