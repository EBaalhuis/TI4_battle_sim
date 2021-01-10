import random
import copy
import app.units as units


IT = 10000


def generate_hits(units):
    result = 0
    for u in units:
        for val in u.combat:
            x = random.randint(1, 10)
            if x >= val:
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
            for val in u.bombard:
                x = random.randint(1, 10)
                if x >= val:
                    result += 1
    return result


def antifighter(units):
    result = 0
    for u in units:
        for val in u.afb:
            x = random.randint(1, 10)
            if x >= val:
                result += 1
    return result


def assign_afb(units, hits):
    for u in units:
        if hits == 0:
            return units
        if u.fighter:
            units.remove(u)
            hits -= 1
    return units


def space_cannon(units):
    result = 0
    for u in units:
        for val in u.cannon:
            x = random.randint(1, 10)
            if x >= val:
                result += 1
    return result


def iteration(att_units, def_units, ground_combat):
    # 0 - tie
    # 1 - attacker won
    # 2 - defender won

    # space cannon offense
    if not ground_combat:
        att_cannon_hits = space_cannon(att_units)
        def_cannon_hits = space_cannon(def_units)
        att_units = assign_hits(att_units, def_cannon_hits)
        def_units = assign_hits(def_units, att_cannon_hits)

    # anti-fighter barrage
    if not ground_combat:
        att_afb = antifighter(att_units)
        def_afb = antifighter(def_units)
        att_units = assign_afb(att_units, def_afb)
        def_units = assign_afb(def_units, att_afb)

    # bombardment
    if ground_combat:
        bombard_hits = bombardment(att_units)
        def_units = assign_hits(def_units, bombard_hits)

    # space cannon defense
    if ground_combat:
        cannon_hits = space_cannon(def_units)
        att_units = assign_hits(att_units, cannon_hits)

    # remove PDS as they do not participate in combat (cannot be assigned hits)
    att_units = list(filter(lambda x: not x.pds, att_units))
    def_units = list(filter(lambda x: not x.pds, def_units))

    while att_units and def_units:
        att_units, def_units = combat_round(att_units, def_units)

    if not att_units and not def_units:
        return 0
    elif not att_units:
        return 2
    elif not def_units:
        return 1


def shield_active(att_units, def_units):
    for u in att_units:
        if u.disable_shield:
            return False

    for u in def_units:
        if u.shield:
            return True

    return False


def filter_ground(att_units, def_units):
    att_res, def_res = [], []

    shield = shield_active(att_units, def_units)
    for u in att_units:
        if u.ground:
            att_res.append(u)
        elif u.bombard and not shield:
            u.combat = []  # disable combat
            att_res.append(u)

    for u in def_units:
        if u.ground or u.cannon:
            def_res.append(u)

    return att_res, def_res


def filter_space(att_units, def_units):
    return list(filter(lambda x: not x.ground, att_units)), list(filter(lambda x: not x.ground, def_units))


def run_simulation(att_units, def_units, it=IT, ground_combat=False):
    outcomes = [0, 0, 0]

    if ground_combat:
        att_units, def_units = filter_ground(att_units, def_units)
    else:
        att_units, def_units = filter_space(att_units, def_units)

    for i in range(it):
        res = iteration(copy.deepcopy(att_units), copy.deepcopy(def_units), ground_combat)
        outcomes[res] += 1

    return outcomes


def print_results(outcomes, it=IT):
    print("Attacker wins: %.1f%%" % (outcomes[1] / it * 100))
    print("Tie: %.1f%%" % (outcomes[0] / it * 100))
    print("Defender wins: %.1f%%" % (outcomes[2] / it * 100))


def parse_units(unit_dict, faction):
    return [units.flagship(faction)] * unit_dict["flagship"] + \
           [units.warsun(faction)] * unit_dict["warsun"] + \
           [units.cruiser(faction)] * unit_dict["cruiser"] + \
           [units.dread(faction)] * unit_dict["dread"] + \
           [units.destroyer(faction)] * unit_dict["destroyer"] + \
           [units.pds(faction)] * unit_dict["pds"] + \
           [units.carrier(faction)] * unit_dict["carrier"] + \
           [units.fighter(faction)] * unit_dict["fighter"] + \
           [units.infantry(faction)] * unit_dict["inf"] + \
           [units.mech(faction)] * unit_dict["mech"]


def calculate(attacker, defender, options):
    att_units = parse_units(attacker, options["att_faction"])
    def_units = parse_units(defender, options["def_faction"])

    outcomes = run_simulation(att_units, def_units, ground_combat=options["ground_combat"])

    return list(map(lambda x: round(x/IT*100, 1), outcomes))
