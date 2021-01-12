import random
import copy
import app.units as units
from app.factions import *


IT = 10000


def has_flagship(units):
    return len(list(filter(lambda x: x.name == "flagship", units))) > 0


def generate_hits(units, faction):
    result = 0
    for u in units:
        for val in u.combat:
            x = random.randint(1, 10)
            if x >= val:
                result += 1

            # Jol-Nar flagsip
            if faction == "Jol-Nar" and u.name == "flagship":
                if x >= 9:
                    result += 2

            # Sardakk flagship
            if faction == "Sardakk" and has_flagship(units) and u.name != "flagship":
                if x == val - 1:
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


def assign_fighters_only(units, hits):
    for u in units:
        if hits == 0:
            return units
        if u.fighter:
            units.remove(u)
            hits -= 1
    return units


def assign_nonfighters_first(units, hits):
    for u in units:
        if hits == 0:
            return units
        if u.sustain:
            u.sustain = False
            hits -= 1

    for u in units:
        if hits == 0:
            return units
        if u.name != "fighter":
            units.remove(u)
            hits -= 1

    for u in units:
        if hits == 0:
            return units
        units.remove(u)
        hits -= 1

    return units


def combat_round(att_units, def_units, options):
    # Winnu flagship
    if options["att_faction"] == "Winnu" or options["def_faction"] == "Winnu":
        att_units, def_units = winnu_flagship(att_units, def_units, options)

    att_hits = generate_hits(att_units, options["att_faction"])
    def_hits = generate_hits(def_units, options["def_faction"])

    # Sardakk mech
    if options["att_faction"] == "Sardakk" or options["def_faction"] == "Sardakk":
        att_hits, def_hits = sardakk_mechs(att_units, def_units, att_hits, def_hits, options)

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


def space_cannon(units):
    result = 0
    for u in units:
        for val in u.cannon:
            x = random.randint(1, 10)
            if x >= val:
                result += 1
    return result


def filter_bombardment(units):
    return list(filter(lambda x: x.ground, units))


def iteration(att_units, def_units, options):
    # 0 - tie
    # 1 - attacker won
    # 2 - defender won

    # space cannon offense
    if not options["ground_combat"]:
        att_cannon_hits = space_cannon(att_units)
        def_cannon_hits = space_cannon(def_units)
        if options["def_graviton"]:
            att_units = assign_nonfighters_first(att_units, def_cannon_hits)
        else:
            att_units = assign_hits(att_units, def_cannon_hits)
        if options["att_graviton"]:
            def_units = assign_nonfighters_first(def_units, att_cannon_hits)
        else:
            def_units = assign_hits(def_units, att_cannon_hits)

    # anti-fighter barrage
    if not options["ground_combat"]:
        att_afb_hits = antifighter(att_units)
        def_afb_hits = antifighter(def_units)
        att_units = assign_fighters_only(att_units, def_afb_hits)
        def_units = assign_fighters_only(def_units, att_afb_hits)

    # bombardment
    if options["ground_combat"]:
        bombard_hits = bombardment(att_units)
        def_units = assign_hits(def_units, bombard_hits)
        att_units = filter_bombardment(att_units)

    # space cannon defense
    if options["ground_combat"]:
        cannon_hits = space_cannon(def_units)
        att_units = assign_hits(att_units, cannon_hits)

    # remove PDS as they do not participate in combat (cannot be assigned hits)
    att_units = list(filter(lambda x: not x.pds, att_units))
    def_units = list(filter(lambda x: not x.pds, def_units))

    while att_units and def_units:
        att_units, def_units = combat_round(att_units, def_units, options)

    if not att_units and not def_units:
        return 0
    elif not att_units:
        return 2
    elif not def_units:
        return 1


def shield_active(att_units, def_units, options):
    for u in att_units:
        if u.disable_shield:
            return False

    for u in def_units:
        if u.shield:
            return True

    return False


def filter_ground(att_units, def_units, options):
    att_res, def_res = [], []

    shield = shield_active(att_units, def_units, options)
    for u in att_units:
        if u.ground:
            att_res.append(u)
        elif u.bombard and not shield:
            att_res.append(u)

    for u in def_units:
        if u.ground or u.cannon:
            def_res.append(u)

    return att_res, def_res


def filter_space(att_units, def_units, options):
    return list(filter(lambda x: not x.ground, att_units)), list(filter(lambda x: not x.ground, def_units))


def run_simulation(att_units, def_units, options, it=IT):
    outcomes = [0, 0, 0]

    if options["ground_combat"]:
        att_units, def_units = filter_ground(att_units, def_units, options)
    else:
        att_units, def_units = filter_space(att_units, def_units, options)

        # Argent flagship
        if options["att_faction"] == "Argent" or options["def_faction"] == "Argent":
            att_units, def_units = argent_flagship(att_units, def_units, options)

        # Mentak flagship
        if options["att_faction"] == "Mentak" or options["def_faction"] == "Mentak":
            att_units, def_units = mentak_flagship(att_units, def_units, options)

    # Antimass Deflectors
    if options["att_antimass"]:
        for u in def_units:
            u.cannon = [x+1 for x in u.cannon]
    if options["def_antimass"]:
        for u in att_units:
            u.cannon = [x + 1 for x in u.cannon]

    for i in range(it):
        res = iteration(copy.deepcopy(att_units), copy.deepcopy(def_units), options)
        outcomes[res] += 1

    return outcomes


def print_results(outcomes, it=IT):
    print("Attacker wins: %.1f%%" % (outcomes[1] / it * 100))
    print("Tie: %.1f%%" % (outcomes[0] / it * 100))
    print("Defender wins: %.1f%%" % (outcomes[2] / it * 100))


def parse_units(unit_dict, faction):

    return [units.fighter(faction) for i in range(unit_dict["fighter"])] + \
           [units.carrier(faction) for i in range(unit_dict["carrier"])] + \
           [units.destroyer(faction) for i in range(unit_dict["destroyer"])] + \
           [units.cruiser(faction) for i in range(unit_dict["cruiser"])] + \
           [units.dread(faction) for i in range(unit_dict["dread"])] + \
           [units.flagship(faction) for i in range(unit_dict["flagship"])] + \
           [units.warsun(faction) for i in range(unit_dict["warsun"])] + \
           [units.pds(faction) for i in range(unit_dict["pds"])] + \
           [units.infantry(faction) for i in range(unit_dict["infantry"])] + \
           [units.mech(faction) for i in range(unit_dict["mech"])]


def calculate(attacker, defender, options):
    att_units = parse_units(attacker, options["att_faction"])
    def_units = parse_units(defender, options["def_faction"])

    outcomes = run_simulation(att_units, def_units, options)

    return list(map(lambda x: round(x/IT*100, 1), outcomes))
