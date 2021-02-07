def dimensional_splicer(units):
    # Take 1 hit, assigned by opponent
    # Prefer to assign to ships that cannot sustain, and prefer less expendable ship
    result = [u for u in units]
    for u in reversed(units):
        if not u.sustain and not (u.name == "pds" and not u.ground):
            result.remove(u)
            return result

    # If we get here, all units must have sustain or are PDS
    for u in reversed(result):
        if not (u.name == "pds" and not u.ground):
            u.use_sustain()
            return result

    return result


def noneuclidean(units):
    for u in units:
        if u.can_sustain:
            u.noneuclidean = True

    return units


def assault(units):
    for u in units:
        if not u.fighter:
            units.remove(u)
            return units

    return units


def duranium(units):
    for u in reversed(units):
        if u.can_sustain and not u.sustain and not u.just_sustained:
            u.sustain = True
            break

    for u in units:
        u.just_sustained = False

    return units


def magen_omega(att_units):
    # attacking units take 1 hit, assigned by opponent
    if not att_units:
        return att_units
    if att_units[0].sustain:
        att_units[0].sustain = False
        att_units[0].just_sustained = True
    else:
        del att_units[0]

    return att_units


def x89(def_units, hits):
    # if any infantry is destroyed, all infantry are destroyed

    nr_infantry = len(list(filter(lambda x: x.name == "infantry", def_units)))
    nr_mechs = len(list(filter(lambda x: x.name == "mech", def_units)))

    if hits > 2*nr_mechs:
        # have to lose 1 infantry regardless, so assign as many hits as possible to infantry
        def_units = list(filter(lambda x: x.name == "mech", def_units))
        hits -= nr_infantry

        # sustain on mechs
        for u in def_units:
            if hits == 0:
                return def_units
            hits -= u.use_sustain()

        while hits > 0 and def_units:
            del def_units[0]
            hits -= 1

        return def_units
    elif hits <= nr_mechs:
        # can sustain all hits on mechs
        # sustain on mechs
        for u in def_units:
            if hits == 0:
                return def_units
            hits -= u.use_sustain()
        return def_units
    else:
        # have to choose between losing mechs or all infantry - assign value
        value_infantry = 1
        value_mech_unsustained = 2.3
        value_mech_sustained = 1.7

        # option 1: lose mechs
        mechs_left = 2*nr_mechs - hits
        opt1 = mechs_left * value_mech_sustained + value_infantry * nr_infantry

        # option 2: lose all infantry
        mech_hits = max(0, hits - nr_infantry)
        unsustained_mechs_left = max(0, nr_mechs - mech_hits)
        sustained_mechs_left = mech_hits if mech_hits <= nr_mechs else 2*nr_mechs - mech_hits
        opt2 = unsustained_mechs_left * value_mech_unsustained + sustained_mechs_left * value_mech_sustained

        if opt1 >= opt2:
            # sustain on mechs
            for u in def_units:
                if hits == 0:
                    return def_units
                hits -= u.use_sustain()

            while hits > 0 and def_units:
                del def_units[-1]
                hits -= 1
        else:
            # lose infantry
            while hits > 0 and def_units[0].name == "infantry":
                del def_units[0]
                hits -= 1

            # sustain on mechs
            for u in def_units:
                if hits == 0:
                    return def_units
                hits -= u.use_sustain()

            # lose mechs
            while hits > 0 and def_units:
                del def_units[0]
                hits -= 1

    return def_units
