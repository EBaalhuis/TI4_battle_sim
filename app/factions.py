def argent_flagship(att_units, def_units, options):
    if options["att_faction"] == "Argent":
        def_units = list(filter(lambda x: x.name != "pds", def_units))

    if options["def_faction"] == "Argent":
        att_units = list(filter(lambda x: x.name != "pds", att_units))

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
