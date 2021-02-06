import app.calculator.faction_abilities as faction_abilities


def assign_hits(units, hits, risk_direct_hit, faction, options, attacker):
    # Letnev flagship (sustain)
    if faction == "Letnev":
        units, hits = faction_abilities.letnev_flagship_sustain(units, hits, risk_direct_hit)

    for u in units:
        if hits <= 0:
            return units, options
        hits -= u.use_sustain(risk_direct_hit)

    while hits > 0 and units:
        if units[0].sustain:
            hits -= u.use_sustain(risk_direct_hit=True)
            # Once one ship sustains and is not Direct Hit, assume its safe
            return assign_hits(units, hits, True, faction, options, attacker)
        else:
            # Check if only PDS are left
            if units[0].name == "pds" and not units[0].ground:  # second part rules out Titans PDS
                return units, options

            # Yin agent
            if (options["att_yin_agent_active"] and attacker) or (options["def_yin_agent_active"] and not attacker) \
                    and units[0].name in ["destroyer", "cruiser"]:
                units, options = faction_abilities.yin_agent(units, units[0], faction, options, attacker)
            else:
                del units[0]

            hits -= 1

    return units, options


def assign_fighters_only(units, hits):
    result = [u for u in units]
    for u in units:
        if hits <= 0:
            return result
        if u.fighter or u.name == "virtual":
            result.remove(u)
            hits -= 1
    return result


def assign_nonfighters_first(units, hits, risk_direct_hit, faction, options, attacker):
    # Letnev flagship (sustain)
    if faction == "Letnev":
        units, hits = faction_abilities.letnev_flagship_sustain(units, hits, risk_direct_hit)

    for u in units:
        if hits <= 0:
            return units, options
        hits -= u.use_sustain(risk_direct_hit)

    fighters = list(filter(lambda x: x.name == "fighter", units))
    non_fighters = list(filter(lambda x: x.name != "fighter", units))

    for u in non_fighters:
        if hits <= 0:
            return units, options
        if u.name == "pds" and not u.ground:  # second part rules out Titans PDS
            break
        if u.sustain:
            hits -= u.use_sustain(risk_direct_hit=True)
            # Once one ship sustains and is not Direct Hit, assume its safe
            return assign_nonfighters_first(units, hits, True, faction, options, attacker)
        else:
            # Yin agent
            if (options["att_yin_agent_active"] and attacker) or (options["def_yin_agent_active"] and not attacker) \
                    and units[0].name in ["destroyer", "cruiser"]:
                units, options = faction_abilities.yin_agent(units, u, faction, options, attacker)
            else:
                units.remove(u)

            hits -= 1

    for u in fighters:
        if hits <= 0:
            return units, options
        if u.name == "pds" and not u.ground:  # second part rules out Titans PDS
            return units, options
        units.remove(u)
        hits -= 1

    return units, options