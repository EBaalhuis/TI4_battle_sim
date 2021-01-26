import random
import copy
import app.units as units
from app.faction_abilities import *
from app.tech_abilities import *


IT = 10000


def has_flagship(units):
    return len(list(filter(lambda x: x.name == "flagship", units))) > 0


def generate_hits(units, faction, morale, prototype, fire_team):
    hits = 0
    non_fighter_hits = 0

    for u in units:
        for val in u.combat:
            x = random.randint(1, 10)

            # Jol-Nar flagsip
            if faction == "Jol-Nar" and u.name == "flagship":
                if x >= 9:
                    hits += 2

            # Sardakk flagship
            if faction == "Sardakk" and has_flagship(units) and u.name != "flagship":
                x += 1

            # Morale Boost
            if morale:
                x += 1

            # Prototype Fighter
            if prototype and u.fighter:
                x += 2

            if x >= val:
                # L1Z1X Flagship
                if faction == "L1Z1X" and has_flagship(units) and u.name in ["flagship", "dread"]:
                    non_fighter_hits += 1
                else:
                    hits += 1

            # Fire Team
            elif fire_team:  # re-roll if it was a miss, ground combat only (so no prototype, L1 flagship)
                x = random.randint(1, 10)
                if morale:
                    x += 1
                if x >= val:
                    hits += 1

    return hits, non_fighter_hits


def assign_hits(units, hits, risk_direct_hit):
    for u in units:
        if hits == 0:
            return units
        if u.sustain and (u.direct_hit_immune or risk_direct_hit):
            u.sustain = False
            hits -= 1

    while hits > 0 and units:
        if units[0].sustain:
            units[0].sustain = False
            hits -= 1
        else:
            if units[0].name == "pds" and not units[0].ground:  # second part rules out Titans PDS
                return units
            del units[0]
            hits -= 1

    return units


def assign_fighters_only(units, hits):
    result = [u for u in units]
    for u in units:
        if hits == 0:
            return result
        if u.fighter:
            result.remove(u)
            hits -= 1
    return result


def assign_nonfighters_first(units, hits, risk_direct_hit):
    for u in units:
        if hits == 0:
            return units
        if u.sustain and (u.direct_hit_immune or risk_direct_hit):
            u.sustain = False
            hits -= 1

    fighters = list(filter(lambda x: x.name == "fighter", units))
    non_fighters = list(filter(lambda x: x.name != "fighter", units))

    for u in non_fighters:
        if hits == 0:
            return units
        if u.name == "pds" and not u.ground:  # second part rules out Titans PDS
            break
        if u.sustain:
            if hits > 1:
                units.remove(u)
                hits -= 2
            else:
                u.sustain = False
                hits -= 1
        else:
            units.remove(u)
            hits -= 1

    for u in fighters:
        if hits == 0:
            return units
        if u.name == "pds" and not u.ground:  # second part rules out Titans PDS
            return units
        units.remove(u)
        hits -= 1

    return units


def combat_round(att_units, def_units, first_round, options):
    # Winnu flagship
    if options["att_faction"] == "Winnu" or options["def_faction"] == "Winnu":
        att_units, def_units = winnu_flagship(att_units, def_units, options)

    att_hits, att_nonfighter_hits = generate_hits(att_units, options["att_faction"],
                             morale=(first_round and options["att_morale"]),
                             prototype=(first_round and options["att_prototype"]),
                             fire_team=(options["att_fireteam"] and first_round and options["ground_combat"]))
    def_hits, def_nonfighter_hits = generate_hits(def_units, options["def_faction"],
                             morale=(first_round and options["def_morale"]),
                             prototype=(first_round and options["def_prototype"]),
                             fire_team=(options["def_fireteam"] and first_round and options["ground_combat"]))

    # Magen Defense Grid
    if first_round and options["def_magen"] and options["ground_combat"] and \
            len(list(filter(lambda x: x.shield, def_units))) > 0:
        att_hits = 0

    # remove PDS as they do not participate in combat (cannot be assigned hits)
    att_units = list(filter(lambda x: not x.pds or x.ground, att_units))
    def_units = list(filter(lambda x: not x.pds or x.ground, def_units))

    # Duranium Armor
    if not first_round:
        if options["att_duranium"]:
            duranium(att_units)
        if options["def_duranium"]:
            duranium(def_units)

    # Sardakk mech
    if options["att_faction"] == "Sardakk" or options["def_faction"] == "Sardakk":
        att_hits, def_hits = sardakk_mechs(att_units, def_units, att_hits, def_hits, options)

    att_units = assign_hits(att_units, def_hits, options["att_riskdirecthit"])
    att_units = assign_nonfighters_first(att_units, def_nonfighter_hits, options["att_riskdirecthit"])
    def_units = assign_hits(def_units, att_hits, options["def_riskdirecthit"])
    def_units = assign_nonfighters_first(def_units, att_nonfighter_hits, options["def_riskdirecthit"])

    return att_units, def_units


def bombardment(units, options):
    result = 0
    best_dice = 11
    for u in units:
        if u.bombard:
            for val in u.bombard:
                best_dice = min(best_dice, val)
                x = random.randint(1, 10)
                if options["def_bunker"]:
                    x -= 4
                if x >= val:
                    result += 1

    if options["att_plasma"]:
        x = random.randint(1, 10)
        if options["def_bunker"]:
            x -= 4
        if x >= best_dice:
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


def space_cannon(units, options, attacker):
    result = 0
    best_dice = 11
    for u in units:
        for val in u.cannon:
            best_dice = min(best_dice, val)
            x = random.randint(1, 10)
            if x >= val:
                result += 1

    if (attacker and options["att_plasma"]) or (not attacker and options["def_plasma"]):
        x = random.randint(1, 10)
        if x >= best_dice:
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
        # Experimental Battlestation
        if options["def_experimental"]:
            def_units = [units.experimental_battlestation(options["def_faction"])] + def_units

        att_cannon_hits = space_cannon(att_units, options, attacker=True)
        def_cannon_hits = space_cannon(def_units, options, attacker=False)

        # Maneuvering Jets
        if options["def_maneuvering"]:
            att_cannon_hits = max(0, att_cannon_hits - 1)
        if options["att_maneuvering"]:
            def_cannon_hits = max(0, def_cannon_hits - 1)

        if options["def_graviton"]:
            att_units = assign_nonfighters_first(att_units, def_cannon_hits, options["att_riskdirecthit"])
        else:
            att_units = assign_hits(att_units, def_cannon_hits, options["att_riskdirecthit"])
        if options["att_graviton"]:
            def_units = assign_nonfighters_first(def_units, att_cannon_hits, options["def_riskdirecthit"])
        else:
            def_units = assign_hits(def_units, att_cannon_hits, options["def_riskdirecthit"])

    # Assault Cannon
    if not options["ground_combat"]:
        if options["att_assault"] and len(list(filter(lambda x: x.non_fighter_ship, att_units))) >= 3:
            def_units = assault(def_units)
        if options["def_assault"] and len(list(filter(lambda x: x.non_fighter_ship, def_units))) >= 3:
            att_units = assault(att_units)


    # anti-fighter barrage
    if not options["ground_combat"]:
        att_afb_hits = antifighter(att_units)
        def_afb_hits = antifighter(def_units)
        if options["def_waylay"]:
            att_units = assign_hits(att_units, def_afb_hits, options["att_riskdirecthit"])
        else:
            att_units = assign_fighters_only(att_units, def_afb_hits)
        if options["att_waylay"]:
            def_units = assign_hits(def_units, att_afb_hits, options["def_riskdirecthit"])
        else:
            def_units = assign_fighters_only(def_units, att_afb_hits)

    # bombardment
    if options["ground_combat"]:
        bombard_hits = bombardment(att_units, options)
        if not options["att_x89"]:
            def_units = assign_hits(def_units, bombard_hits, options["def_riskdirecthit"])
        else:
            def_units = x89(def_units, bombard_hits)
        att_units = filter_bombardment(att_units)

    # space cannon defense
    if options["ground_combat"]:
        cannon_hits = space_cannon(def_units, options, attacker=False)

        # Maneuvering Jets
        if options["att_maneuvering"]:
            cannon_hits = max(0, cannon_hits - 1)

        att_units = assign_hits(att_units, cannon_hits, options["att_riskdirecthit"])

    # Magen Defense Grid Omega
    if options["def_magen_o"] and options["ground_combat"]:
        att_units = magen_omega(att_units)

    first_round = True
    while att_units and def_units:
        att_units, def_units = combat_round(att_units, def_units, first_round, options)
        first_round = False

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
    return list(filter(lambda x: not x.ground or len(x.cannon) > 0, att_units)), \
           list(filter(lambda x: not x.ground or len(x.cannon) > 0, def_units))


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

    # Defending in Nebula
    if options["def_nebula"] and not options["ground_combat"]:
        for u in def_units:
            u.combat = [x - 1 for x in u.combat]

    # Antimass Deflectors
    if options["att_antimass"]:
        for u in def_units:
            u.cannon = [x + 1 for x in u.cannon]
    if options["def_antimass"]:
        for u in att_units:
            u.cannon = [x + 1 for x in u.cannon]

    # Conventions of War
    if options["conventions"]:
        for u in att_units:
            u.bombard = []

    # Publicize Weapon Schematics
    if options["publicize"]:
        for u in att_units + def_units:
            if u.name == "warsun":
                u.sustain = False
                u.can_sustain = False

    for i in range(it):
        res = iteration(copy.deepcopy(att_units), copy.deepcopy(def_units), options)

        # Yin flagship
        if options["att_faction"] == "Yin" and has_flagship(att_units) and res == 2:
            res = 0
        if options["def_faction"] == "Yin" and has_flagship(def_units) and res == 1:
            res = 0

        outcomes[res] += 1

    return outcomes


def print_results(outcomes, it=IT):
    print("Attacker wins: %.1f%%" % (outcomes[1] / it * 100))
    print("Tie: %.1f%%" % (outcomes[0] / it * 100))
    print("Defender wins: %.1f%%" % (outcomes[2] / it * 100))


def parse_unit(unit_type, unit_dict, attacker, options):
    prefix = "att_" if attacker else "def_"

    faction = options[prefix + "faction"]
    amount = unit_dict[unit_type]
    upgraded = options[prefix + unit_type + "2"]

    if unit_type == "fighter":
        func = units.fighter2 if upgraded else units.fighter
    elif unit_type == "carrier":
        func = units.carrier2 if upgraded else units.carrier
    elif unit_type == "destroyer":
        func = units.destroyer2 if upgraded else units.destroyer
    elif unit_type == "cruiser":
        func = units.cruiser2 if upgraded else units.cruiser
    elif unit_type == "dread":
        func = units.dread2 if upgraded else units.dread
    elif unit_type == "flagship":
        func = units.flagship2 if upgraded else units.flagship
    elif unit_type == "warsun":
        func = units.warsun2 if upgraded else units.warsun
    elif unit_type == "infantry":
        func = units.infantry2 if upgraded else units.infantry
    elif unit_type == "mech":
        func = units.mech2 if upgraded else units.mech
    elif unit_type == "pds":
        func = units.pds2 if upgraded else units.pds

    return [func(faction) for _ in range(amount)]


def parse_units(unit_dict, attacker, options):
    unit_types = ["fighter", "carrier", "destroyer", "cruiser", "dread", "infantry", "mech", "flagship", "warsun", 
                  "pds"]
    result = []
    for u in unit_types:
        result = result + parse_unit(u, unit_dict, attacker, options)

    return result


def calculate(attacker_units, defender_units, options):
    att_units = parse_units(attacker_units, attacker=True, options=options)
    def_units = parse_units(defender_units, attacker=False, options=options)

    outcomes = run_simulation(att_units, def_units, options)

    return list(map(lambda x: round(x/IT*100, 1), outcomes))
