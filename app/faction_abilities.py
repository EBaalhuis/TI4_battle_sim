def magen_omega(att_units):
    # attacking units take 1 hit, assigned by opponent
    if att_units[0].sustain:
        att_units[0].sustain = False
    else:
        del att_units[0]

    return att_units


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
                u.combat = [7] * len(def_units)

    if options["def_faction"] == "Winnu":
        for u in def_units:
            if u.name == "flagship":
                u.combat = [7] * len(att_units)

    return att_units, def_units
