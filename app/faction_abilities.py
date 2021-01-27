from app.units import Unit


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
