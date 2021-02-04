import random
from app.units import Unit, fighter, fighter2


def naalu_nekro_mech(units):
    for u in units:
        if u.name == "mech":
            u.combat = [value - 2 for value in u.combat]
    return units


def yin_agent(units, u, faction, options, attacker):
    # u got destroyed and is a cruiser or destroyer; replace with 2 fighters
    units.remove(u)

    if attacker:
        options["att_yin_agent_active"] = False
    else:
        options["def_yin_agent_active"] = False

    upgraded = options["att_fighter2"] if attacker else options["def_fighter2"]
    fighters = [fighter2(faction), fighter2(faction)] if upgraded else [fighter(faction), fighter(faction)]

    return fighters + units, options


def titans_agent(units):
    # The Titans agent cancels one hit. Assume it is the first hit that would kill a unit, by prepending a
    # virtual unit
    virtual_unit = Unit("virtual", [], ground=True)
    return [virtual_unit] + units


def cavalry(units, upgraded):
    eligible = [u for u in units if not u.fighter and not u.pds]
    if not eligible:
        return units
    else:
        replacing = eligible[0]
        replacing.can_sustain = True
        replacing.sustain = True
        replacing.combat = [5, 5] if upgraded else [7, 7]
        replacing.afb = [5, 5, 5] if upgraded else [8, 8, 8]
        result = [u for u in units if u.name not in ["warsun", "flagship"] and u != replacing] + [replacing] + \
            [u for u in units if u.name in ["warsun", "flagship"] and u != replacing]
        return result


def winnu_commander(units):
    for u in units:
        u.combat = [x - 2 for x in u.combat]

    return units


def apply_letnev_agent(units):
    best = 11
    best_unit = False
    for u in units:
        if min(u.combat) < best:
            best = min(u.combat)
            best_unit = u
    best_unit.combat = best_unit.combat + best_unit.combat[0:1]

    return units, best_unit


def apply_sol_agent(units):
    return apply_letnev_agent(units)


def raid_formation(att_units, def_units, att_afb_hits, def_afb_hits, options):
    if options["att_faction"] == "Argent":
        damage = max(0, att_afb_hits - len(list(filter(lambda x: x.fighter, def_units))))
        for u in def_units:
            if damage == 0:
                break
            if u.sustain:
                u.sustain = False
                damage -= 1

    if options["def_faction"] == "Argent":
        damage = max(0, def_afb_hits - len(list(filter(lambda x: x.fighter, att_units))))
        for u in att_units:
            if damage == 0:
                break
            if u.sustain:
                u.sustain = False
                damage -= 1

    return att_units, def_units


def assign_swa2(units, hits):
    # These hits are assigned to infantry only
    result = [u for u in units]
    for u in units:
        if hits == 0:
            return result
        if u.name == "infantry":
            result.remove(u)
            hits -= 1
    return result


def check_letnev_flagship(units):
    for u in units:
        if u.name == "flagship":
            return u

    return False


def letnev_flagship(att_units, def_units, options):
    if options["att_faction"] == "Letnev":
        for u in att_units:
            if u.name == "flagship" and u.can_sustain:
                u.sustain = True

    if options["def_faction"] == "Letnev":
        for u in def_units:
            if u.name == "flagship" and u.can_sustain:
                u.sustain = True

    return att_units, def_units


def tekklar(att_units, def_units, options):
    if options["att_tekklar"]:
        for u in att_units:
            u.combat = [x - 1 for x in u.combat]
        if options["def_faction"] == "Sardakk":
            for u in def_units:
                u.combat = [x + 1 for x in u.combat]

    if options["def_tekklar"]:
        for u in def_units:
            u.combat = [x - 1 for x in u.combat]
        if options["att_faction"] == "Sardakk":
            for u in att_units:
                u.combat = [x + 1 for x in u.combat]

    return att_units, def_units


def apply_argent_prom(units, options, attacker):
    if options["ground_combat"] and attacker:
        # apply to bombardment
        best_unit = False
        best_bombard = 11
        for u in units:
            if len(u.bombard) > 0 and min(u.bombard) < best_bombard:
                best_bombard = min(u.bombard)
                best_unit = u
        if best_unit:
            best_unit.bombard = best_unit.bombard + best_unit.bombard[0:1]
    elif options["ground_combat"] and not attacker:
        # apply to space cannon defense/offense
        best_unit = False
        best_cannon = 11
        for u in units:
            if len(u.cannon) > 0 and min(u.cannon) < best_cannon:
                best_cannon = min(u.cannon)
                best_unit = u
        if best_unit:
            best_unit.cannon = best_unit.cannon + best_unit.cannon[0:1]
    else:
        # space combat - have to check if space cannon offense or AFB is better
        best_cannon_unit = False
        best_cannon = 11
        best_afb_unit = False
        best_afb = 11
        for u in units:
            if len(u.cannon) > 0 and min(u.cannon) < best_cannon:
                best_cannon = min(u.cannon)
                best_cannon_unit = u
            if len(u.afb) > 0 and min(u.afb) < best_afb:
                best_afb = min(u.afb)
                best_afb_unit = u
        if best_cannon_unit and best_cannon <= best_afb:
            best_cannon_unit.cannon = best_cannon_unit.cannon + best_cannon_unit.cannon[0:1]
        elif best_afb_unit:
            best_afb_unit.afb = best_afb_unit.afb + best_afb_unit.afb[0:1]

    return units


def argent_prom(att_units, def_units, options):
    if options["att_argent_prom"]:
        att_units = apply_argent_prom(att_units, options, attacker=True)
    if options["def_argent_prom"]:
        def_units = apply_argent_prom(def_units, options, attacker=False)
    return att_units, def_units


def generate_ambush_hits(units):
    hits = 0
    fired = 0
    cruisers = list(filter(lambda x: x.name == "cruiser", units))
    destroyers = list(filter(lambda x: x.name == "destroyer", units))

    if len(cruisers) >= 2:
        val = cruisers[0].combat[0]
        for _ in range(2):
            x = random.randint(1, 10)
            if x >= val:
                hits += 1
        return hits
    elif len(cruisers) == 1:
        fired = 1
        val = cruisers[0].combat[0]
        x = random.randint(1, 10)
        if x >= val:
            hits += 1

    if fired == 0 and len(destroyers) >= 2:
        val = destroyers[0].combat[0]
        for _ in range(2):
            x = random.randint(1, 10)
            if x >= val:
                hits += 1
    elif fired < 2 and len(destroyers) >= 1:
        val = destroyers[0].combat[0]
        x = random.randint(1, 10)
        if x >= val:
            hits += 1

    return hits


def mentak_mech(att_units, def_units, options):
    if options["att_faction"] == "Mentak":
        for u in def_units:
            u.sustain = False

    if options["def_faction"] == "Mentak":
        for u in att_units:
            u.sustain = False

    return att_units, def_units


def mentak_ambush(att_units, def_units, options):
    att_hits = 0
    def_hits = 0

    if options["att_faction"] == "Mentak":
        att_hits = generate_ambush_hits(att_units)
    if options["def_faction"] == "Mentak":
        def_hits = generate_ambush_hits(def_units)

    return att_hits, def_hits


def jol_nar_mech(units):
    for u in units:
        if u.name == "infantry":
            u.combat = [x - 1 for x in u.combat]
    return units


def naaz_mech():
    return Unit("mech", [8, 8])


def naalu_flagship(units):
    result = list(filter(lambda x: x.fighter, units))
    for u in result:
        u.ground = True
    return result


def naaz_flagship(units):
    for u in units:
        if u.name == "mech":
            u.combat = u.combat + [u.combat[0]]
    return units


def argent_flagship(att_units, def_units, options):
    if options["att_faction"] == "Argent":
        if len(list(filter(lambda x: x.name == "flagship", att_units))) > 0:
            def_units = list(filter(lambda x: x.name != "pds", def_units))

    if options["def_faction"] == "Argent":
        if len(list(filter(lambda x: x.name == "flagship", def_units))) > 0:
            att_units = list(filter(lambda x: x.name != "pds", att_units))

    return att_units, def_units


def mentak_flagship(att_units, def_units, options):
    if options["att_faction"] == "Mentak":
        for u in def_units:
            u.sustain = False
            u.can_sustain = False

    if options["def_faction"] == "Mentak":
        for u in att_units:
            u.sustain = False
            u.can_sustain = False

    return att_units, def_units


def sardakk_mechs(att_units, def_units, att_hits, def_hits, options):
    if not options["ground_combat"]:
        return att_hits, def_hits

    if options["att_faction"] == "Sardakk":
        extra_hits = min(def_hits, len(list(filter(lambda x: x.name == "mech" and x.sustain, att_units))))
        return att_hits + extra_hits, def_hits

    if options["def_faction"] == "Sardakk":
        extra_hits = min(att_hits, len(list(filter(lambda x: x.name == "mech" and x.sustain, def_units))))
        return att_hits, def_hits + extra_hits

    return att_hits, def_hits


def winnu_flagship(att_units, def_units, options):
    if options["att_faction"] == "Winnu":
        for u in att_units:
            if u.name == "flagship":
                u.combat = [7] * len(list(
                    filter(lambda x: x.name not in ["pds", "fighter"], def_units)))

    if options["def_faction"] == "Winnu":
        for u in def_units:
            if u.name == "flagship":
                u.combat = [7] * len(list(
                    filter(lambda x: x.name not in ["pds", "fighter"], att_units)))

    return att_units, def_units
