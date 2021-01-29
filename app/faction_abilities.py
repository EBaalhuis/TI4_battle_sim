import random
from app.units import Unit


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
    else:
        # apply to space cannon defense/offense
        best_unit = False
        best_cannon = 11
        for u in units:
            if len(u.cannon) > 0 and min(u.cannon) < best_cannon:
                best_cannon = min(u.cannon)
                best_unit = u
        if best_unit:
            best_unit.cannon = best_unit.cannon + best_unit.cannon[0:1]

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

    if options["def_faction"] == "Mentak":
        for u in att_units:
            u.sustain = False

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
                    filter(lambda x: not x.ground and x.name not in ["pds", "fighter"], def_units)))

    if options["def_faction"] == "Winnu":
        for u in def_units:
            if u.name == "flagship":
                u.combat = [7] * len(list(
                    filter(lambda x: not x.ground and x.name not in ["pds", "fighter"], att_units)))

    return att_units, def_units
